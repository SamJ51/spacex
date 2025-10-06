from .helper_functions import api_request
from .models import CrewMember, Payload, Dragon, Launch, LaunchCore, LaunchLinks, PatchLinks, RedditLinks, FlickrLinks

def populate_crew():
    api_url = "https://api.spacexdata.com/v4/crew"
    crew_members = api_request(api_url)
    for p in crew_members:
        CrewMember.objects.get_or_create(
        member_id=p["id"],
        defaults={
            "name": p["name"],
            "agency": p["agency"],
            "image_url": p["image"],
            "wikipedia_url": p["wikipedia"],
            "launches": p["launches"],
            "status": p["status"],
        },)
        
def populate_launch():
    api_url = "https://api.spacexdata.com/v5/launches"
    launches = api_request(api_url)

    for l_data in launches:
        links_data = l_data.get('links', {})
        patch_links_obj, reddit_links_obj, flickr_links_obj = None, None, None

        if links_data and links_data.get('patch'):
            patch_links_obj, _ = PatchLinks.objects.get_or_create(**links_data['patch'])

        if links_data and links_data.get('reddit'):
            reddit_links_obj, _ = RedditLinks.objects.get_or_create(**links_data['reddit'])

        if links_data and links_data.get('flickr'):
            flickr_links_obj, _ = FlickrLinks.objects.get_or_create(**links_data['flickr'])

        launch_links_obj = LaunchLinks.objects.create(
            patch=patch_links_obj,
            reddit=reddit_links_obj,
            flickr=flickr_links_obj,
            presskit=links_data.get('presskit'),
            webcast=links_data.get('webcast'),
            youtube_id=links_data.get('youtube_id'),
            article=links_data.get('article'),
            wikipedia=links_data.get('wikipedia')
        )

        launch_obj = Launch.objects.update_or_create(
            launch_id=l_data['id'],
            defaults={
                'fairings': l_data.get('fairings'),
                'links': launch_links_obj,
                'static_fire_date_utc': l_data.get('static_fire_date_utc'),
                'static_fire_date_unix': l_data.get('static_fire_date_unix'),
                'net': l_data.get('net', False),
                'window': l_data.get('window'),
                'rocket': l_data.get('rocket'),
                'success': l_data.get('success'),
                'failures': l_data.get('failures', []),
                'details': l_data.get('details'),
                'ships': l_data.get('ships', []),
                'capsules': l_data.get('capsules', []),
                'launchpad': l_data.get('launchpad'),
                'flight_number': l_data.get('flight_number'),
                'name': l_data.get('name'),
                'date_utc': l_data.get('date_utc'),
                'date_unix': l_data.get('date_unix'),
                'date_local': l_data.get('date_local'),
                'date_precision': l_data.get('date_precision'),
                'upcoming': l_data.get('upcoming'),
                'auto_update': l_data.get('auto_update'),
                'tdb': l_data.get('tdb', False),
            }
        )

        # Create LaunchCore objects and associate them
        core_objects = []
        for core_data in l_data.get('cores', []):
            core_obj, _ = LaunchCore.objects.get_or_create(
                core=core_data.get('core'),
                flight=core_data.get('flight'),
                defaults=core_data
            )
            core_objects.append(core_obj)
        if core_objects:
            launch_obj.cores.set(core_objects)

        # Link existing CrewMember objects
        crew_ids = l_data.get('crew', [])
        if crew_ids:
            crew_members = CrewMember.objects.filter(member_id__in=crew_ids)
            launch_obj.crew.set(crew_members)

        # Link existing Payload objects
        payload_ids = l_data.get('payloads', [])
        if payload_ids:
            payloads = Payload.objects.filter(payload_id__in=payload_ids)
            launch_obj.payloads.set(payloads)        

def populate_payload():
    api_url = "https://api.spacexdata.com/v4/payloads"
    payloads = api_request(api_url)
    for p in payloads:
        Payload.objects.get_or_create(
            payload_id=p['id'],
            defaults={
                "name": p["name"],
                "type": p["type"],
                "reused": p["reused"],
                "launch": p["launch"],
                "customers": p["customers"],
                "nationalities": p["nationalities"],
                "manufacturers": p["manufacturers"],
                "norad_ids": p["norad_ids"],
                "mass_kg": p["mass_kg"],
                "mass_lbs": p["mass_lbs"],
                "orbit": p["orbit"],
                "reference_system": p["reference_system"],
                "regime": p["regime"],
                "longitude": p["longitude"],
                "semi_major_axis_km": p["semi_major_axis_km"],
                "eccentricity": p["eccentricity"],
                "periapsis_km": p["periapsis_km"],
                "apoapsis_km": p["apoapsis_km"],
                "inclination_deg": p["inclination_deg"],
                "period_min": p["period_min"],
                "lifespan_years": p["lifespan_years"],
                "epoch": p["epoch"],
                "mean_motion": p["mean_motion"],
                "raan": p["raan"],
                "arg_of_pericenter": p["arg_of_pericenter"],
                "mean_anomaly": p["mean_anomaly"],
            },
        )
        
        d = p["dragon"]
        Dragon.objects.get_or_create(
            defaults={
                "capsule": d["capsule"],
                "mass_returned_kg": d["mass_returned_kg"],
                "mass_returned_lbs": d["mass_returned_lbs"],
                "flight_time_sec": d["flight_time_sec"],
                "manifest": d["manifest"],
                "water_landing": d["water_landing"],
                "land_landing": d["land_landing"],
            },
        )