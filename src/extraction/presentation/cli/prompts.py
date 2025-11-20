
from pyfiglet import Figlet
from extraction.application.ports.geoname_query_port import GeoNameQueryPort
from extraction.domain.value_objects.country import Country
from geonames.application.services.geoname_query_service import GeoNameQueryService

def print_banner(text):
    f = Figlet(font='slant')  # o 'standard', 'doom', 'banner3-D', etc.
    print("\033[96m" + f.renderText(text) + "\033[0m")

def prompt_main_menu():
    print_banner("Google Maps Extractor")
    print("MENU")
    print("--")
    print("1) Run new extraction job")
    print("2) Resume pending extraction jobs")
    print("3) Delete an extraction job")
    print("0) Exit")
    print()

def prompt_for_search_seed() -> str:
    while True:
        seed = input("\n🔍 Enter what you want to search for (e.g. restaurants): ").strip()
        if seed:
            return seed
        print("⚠️ The search seed cannot be empty. Please try again.")

def prompt_for_country(geoname_query: GeoNameQueryPort) -> Country | None:
    while True:
        code = input("\n🌎 Country code (2 letters): ").strip().upper()
        countries = geoname_query.find_countries({"isoAlpha2": code})
        if countries:
            return countries[0]
        print("⚠️ Country not found. Please enter a valid ISO code.")

def prompt_for_depth_level(scraping_scope: str = "country") -> str | None:
    print("\n📍 Select depth level:\n")

    options_by_scope = {
        "worldwide": ["continent", "country", "admin1", "admin2"],
        "continent": ["country", "admin1", "admin2"],
        "country": ["admin1", "admin2", "populated_places"],
        "admin1": ["admin2", "populated_places"],
        "admin2": ["populated_places"],
        "populated_places": [],
    }

    descriptions = {
        "continent": "Each continent (e.g., Europe, North America)",
        "country": "Each country within the selected scope (e.g., Spain, United States)",
        "admin1": "First-level administrative divisions (e.g., States, Regions, Autonomous Communities)",
        "admin2": "Second-level divisions (e.g., Provinces, Counties)",
        "admin3": "Third-level divisions (e.g., Municipalities, Districts)",
        "populated_places": "Individual populated places (e.g., cities, towns, villages)",
    }

    available = options_by_scope.get(scraping_scope, [])
    if not available:
        print("⚙️ This scope does not require a depth level (it’s already the lowest level).")
        return None

    for i, level in enumerate(available, start=1):
        print(f"{i}) {level.replace('_', ' ').title()} – {descriptions[level]}")

    while True:
        try:
            choice = int(input(f"\nEnter an option (1–{len(available)}): ").strip())
            if 1 <= choice <= len(available):
                selected = available[choice - 1]
                return selected
            else:
                print(f"⚠️ Please select a number between 1 and {len(available)}.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

def prompt_for_min_population(depth_level: str = "populated_places") -> int | None:
    """
    Ask the user to select the minimum population threshold for populated places.
    This only applies if depth_level == 'populated_places'.
    """

    default_min_population = 15000
    if depth_level != "populated_places":
        return default_min_population

    print("\n🏙️   Select the minimum population threshold for populated places.")
    print("    A higher population means fewer locations and faster completion.\n")

    options = [15000, 5000, 1500, 1000, 500]

    for i, value in enumerate(options, start=1):
        print(f"{i}) {value:,} inhabitants")

    while True:
        try:
            choice = int(input(f"\nEnter a number (1–{len(options)}): ").strip())
            if 1 <= choice <= len(options):
                min_population_selected = options[choice - 1]
                return min_population_selected
            else:
                print(f"⚠️  Please select a number between 1 and {len(options)}.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

def prompt_for_min_rating() -> float:
    """
    Ask the user to select the minimum rating threshold for places.
    A higher value means fewer but better-rated results.
    """
    print("\n⭐  Select the minimum rating for places to include.")
    print("    A higher value means fewer but better-rated results.\n")

    options = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    for i, rating in enumerate(options, start=1):
        print(f"{i}) {rating} stars")

    while True:
        try:
            choice = int(input(f"\nEnter a number (1–{len(options)}): ").strip())
            if 1 <= choice <= len(options):
                selected = options[choice - 1]
                return selected
            else:
                print(f"⚠️  Please select a number between 1 and {len(options)}.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

def prompt_for_max_results() -> int:
    """
    Ask the user to select the maximum number of results to scrape per location.
    A higher value means more results but longer runtime.
    """
    print("\n🔢  Select the maximum number of results to scrape per location.")
    print("    A higher number means more results but longer runtime.\n")

    options = [10, 25, 50, 100, None]

    for i, value in enumerate(options, start=1):
        label = "All" if value is None else f"Up to {value} results"
        print(f"{i}) {label}")

    while True:
        try:
            choice = int(input(f"\nEnter a number (1–{len(options)}): ").strip())
            if 1 <= choice <= len(options):
                selected = options[choice - 1]
                label = "all" if selected is None else f"up to {selected}"
                return selected
            else:
                print(f"⚠️  Please select a number between 1 and {len(options)}.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

def prompt_for_max_reviews() -> int:
    """
    Ask the user to select the maximum number of reviews to scrape per place.
    A higher value means more reviews but longer runtime.
    """
    print("\n💬  Select the maximum number of reviews to scrape per place.")
    print("    A higher number means more reviews but longer runtime.\n")

    options = [0, 10, 25, 50]

    for i, value in enumerate(options, start=1):
        label = "No reviews" if value == 0 else f"Up to {value} reviews"
        print(f"{i}) {label}")

    while True:
        try:
            choice = int(input(f"\nEnter a number (1–{len(options)}): ").strip())
            if 1 <= choice <= len(options):
                selected = options[choice - 1]
                label = "no reviews" if selected == 0 else f"up to {selected}"
                return selected
            else:
                print(f"⚠️  Please select a number between 1 and {len(options)}.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

def prompt_for_language_code(languages: list[str]) -> str:
    """
    Ask the user to select a language code from the given list,
    or enter a custom one manually.
    """
    print("\n🗣️ Select the language to use for this scraping.")
    print("   These are the default languages for the selected country:")
    print("   (you can also enter a different language code manually)\n")

    languages = [lang.strip() for lang in languages if lang.strip()]
    if not languages:
        print("⚠️ No predefined languages found for this country.")
        custom = input("Enter a language code manually (e.g. en, es, fr): ").strip().lower()
        return custom or "en"

    for i, lang in enumerate(languages, start=1):
        print(f"{i}) {lang}")

    print(f"{len(languages)+1}) Other (enter a different code)")

    while True:
        try:
            choice = int(input(f"\nEnter a number (1–{len(languages)+1}): ").strip())
            if 1 <= choice <= len(languages):
                selected = languages[choice - 1]
                return selected
            elif choice == len(languages) + 1:
                custom = input("\nEnter custom language code (e.g. en, es, fr): ").strip().lower()
                return custom or "en"
            else:
                print(f"⚠️ Please select a number between 1 and {len(languages)+1}.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
