from .helper_functions import api_request
from .models import CrewMember, Payload, Dragon, Launch, LaunchCore, LaunchLinks, PatchLinks, RedditLinks, FlickrLinks

def populate_crew():
    api_url = "https://api.spacexdata.com/v4/crew"
    crew_members = api_request(api_url)
    for p in crew_members:
        CrewMember.objects.get_or_create(
            member_id=p.get("id"),
            defaults={
                "name": p.get("name"),
                "agency": p.get("agency"),
                "image_url": p.get("image"),
                "wikipedia_url": p.get("wikipedia"),
                "launches": p.get("launches"),
                "status": p.get("status"),
            },
        )
        
def populate_launch():
    api_url = "https://api.spacexdata.com/v5/launches"
    launches = api_request(api_url)

    for l_data in launches:
        links_data = l_data.get("links", {})
        patch_links_obj, reddit_links_obj, flickr_links_obj = None, None, None

        if links_data and links_data.get("patch"):
            patch_links_obj, _ = PatchLinks.objects.get_or_create(**links_data.get("patch", {}))

        if links_data and links_data.get("reddit"):
            reddit_links_obj, _ = RedditLinks.objects.get_or_create(**links_data.get("reddit", {}))

        if links_data and links_data.get("flickr"):
            flickr_links_obj, _ = FlickrLinks.objects.get_or_create(**links_data.get("flickr", {}))

        launch_links_obj = LaunchLinks.objects.create(
            patch=patch_links_obj,
            reddit=reddit_links_obj,
            flickr=flickr_links_obj,
            presskit=links_data.get("presskit"),
            webcast=links_data.get("webcast"),
            youtube_id=links_data.get("youtube_id"),
            article=links_data.get("article"),
            wikipedia=links_data.get("wikipedia"),
        )

        launch_obj, _ = Launch.objects.update_or_create(
            launch_id=l_data.get("id"),
            defaults={
                "fairings": l_data.get("fairings"),
                "links": launch_links_obj,
                "static_fire_date_utc": l_data.get("static_fire_date_utc"),
                "static_fire_date_unix": l_data.get("static_fire_date_unix"),
                "net": l_data.get("net", False),
                "window": l_data.get("window"),
                "rocket": l_data.get("rocket"),
                "success": l_data.get("success"),
                "failures": l_data.get("failures", []),
                "details": l_data.get("details"),
                "ships": l_data.get("ships", []),
                "capsules": l_data.get("capsules", []),
                "launchpad": l_data.get("launchpad"),
                "flight_number": l_data.get("flight_number"),
                "name": l_data.get("name"),
                "date_utc": l_data.get("date_utc"),
                "date_unix": l_data.get("date_unix"),
                "date_local": l_data.get("date_local"),
                "date_precision": l_data.get("date_precision"),
                "upcoming": l_data.get("upcoming"),
                "auto_update": l_data.get("auto_update"),
                "tdb": l_data.get("tdb", False),
            },
        )

        # Create LaunchCore objects and associate them
        core_objects = []
        for core_data in l_data.get("cores", []):
            core_obj, _ = LaunchCore.objects.get_or_create(
                core=core_data.get("core"),
                flight=core_data.get("flight"),
                defaults=core_data,
            )
            core_objects.append(core_obj)
        if core_objects:
            launch_obj.cores.set(core_objects)

        # Link existing CrewMember objects
        crew_ids = l_data.get("crew", [])
        if crew_ids:
            crew_members = CrewMember.objects.filter(member_id__in=crew_ids)
            launch_obj.crew.set(crew_members)

        # Link existing Payload objects
        payload_ids = l_data.get("payloads", [])
        if payload_ids:
            payloads = Payload.objects.filter(payload_id__in=payload_ids)
            launch_obj.payloads.set(payloads)        

def populate_payload():
    api_url = "https://api.spacexdata.com/v4/payloads"
    payloads = api_request(api_url)
    for p in payloads:
        dragon_obj = None
        if d := p.get("dragon"):
            if any(d.values()):
                dragon_obj, _ = Dragon.objects.get_or_create(
                    capsule=d.get("capsule"),
                    manifest=d.get("manifest"),
                    defaults={
                        "mass_returned_kg": d.get("mass_returned_kg"),
                        "mass_returned_lbs": d.get("mass_returned_lbs"),
                        "flight_time_sec": d.get("flight_time_sec"),
                        "water_landing": d.get("water_landing"),
                        "land_landing": d.get("land_landing"),
                    },
                )
                
        Payload.objects.update_or_create(
            payload_id=p.get("id"),
            defaults={
                "name": p.get("name"),
                "type": p.get("type"),
                "reused": p.get("reused"),
                "launch": p.get("launch"),
                "customers": p.get("customers"),
                "nationalities": p.get("nationalities"),
                "manufacturers": p.get("manufacturers"),
                "norad_ids": p.get("norad_ids"),
                "mass_kg": p.get("mass_kg"),
                "mass_lbs": p.get("mass_lbs"),
                "orbit": p.get("orbit"),
                "reference_system": p.get("reference_system"),
                "regime": p.get("regime"),
                "longitude": p.get("longitude"),
                "semi_major_axis_km": p.get("semi_major_axis_km"),
                "eccentricity": p.get("eccentricity"),
                "periapsis_km": p.get("periapsis_km"),
                "apoapsis_km": p.get("apoapsis_km"),
                "inclination_deg": p.get("inclination_deg"),
                "period_min": p.get("period_min"),
                "lifespan_years": p.get("lifespan_years"),
                "epoch": p.get("epoch"),
                "mean_motion": p.get("mean_motion"),
                "raan": p.get("raan"),
                "arg_of_pericenter": p.get("arg_of_pericenter"),
                "mean_anomaly": p.get("mean_anomaly"),
                "dragon": dragon_obj,
            },
        )