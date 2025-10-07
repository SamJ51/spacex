from django.db import models

class CrewMember(models.Model):
    '''
    Represents a single crew member
    '''
    name = models.CharField(max_length=100, null=True, blank=True)
    agency = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    wikipedia_url = models.URLField(max_length=200, null=True, blank=True)
    launches = models.JSONField(default=list, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    member_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Dragon(models.Model):
    """
    Represents the 'dragon' nested object in the payload data.
    Linked to a single Payload instance.
    """
    capsule = models.CharField(max_length=255, null=True, blank=True)
    mass_returned_kg = models.FloatField(null=True, blank=True)
    mass_returned_lbs = models.FloatField(null=True, blank=True)
    flight_time_sec = models.IntegerField(null=True, blank=True)
    manifest = models.URLField(null=True, blank=True)
    water_landing = models.BooleanField(null=True, blank=True)
    land_landing = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Dragon Capsule {self.capsule}" if self.capsule else f"Dragon (ID: {self.id})"


class Payload(models.Model):
    """
    Represents a single payload
    """
    payload_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    reused = models.BooleanField(default=False, null=True, blank=True)
    launch = models.CharField(max_length=255, null=True, blank=True)
    customers = models.JSONField(default=list, null=True, blank=True)
    nationalities = models.JSONField(default=list, null=True, blank=True)
    manufacturers = models.JSONField(default=list, null=True, blank=True)
    norad_ids = models.JSONField(default=list, null=True, blank=True)
    mass_kg = models.FloatField(null=True, blank=True)
    mass_lbs = models.FloatField(null=True, blank=True)
    orbit = models.CharField(max_length=50, null=True, blank=True)
    reference_system = models.CharField(max_length=50, null=True, blank=True)
    regime = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    semi_major_axis_km = models.FloatField(null=True, blank=True)
    eccentricity = models.FloatField(null=True, blank=True)
    periapsis_km = models.FloatField(null=True, blank=True)
    apoapsis_km = models.FloatField(null=True, blank=True)
    inclination_deg = models.FloatField(null=True, blank=True)
    period_min = models.FloatField(null=True, blank=True)
    lifespan_years = models.IntegerField(null=True, blank=True)
    epoch = models.DateTimeField(null=True, blank=True)
    mean_motion = models.FloatField(null=True, blank=True)
    raan = models.FloatField(null=True, blank=True)
    arg_of_pericenter = models.FloatField(null=True, blank=True)
    mean_anomaly = models.FloatField(null=True, blank=True)

    # Linked Dragon Object
    dragon = models.ForeignKey(
        Dragon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
    
class PatchLinks(models.Model):
    """
    Represents the 'patch' nested object within 'links'.
    """
    small = models.URLField(max_length=200, null=True, blank=True)
    large = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Patch Links (Small: {self.small or 'N/A'})"


class RedditLinks(models.Model):
    """
    Represents the 'reddit' nested object within 'links'.
    """
    campaign = models.URLField(max_length=200, null=True, blank=True)
    launch = models.URLField(max_length=200, null=True, blank=True)
    media = models.URLField(max_length=200, null=True, blank=True)
    recovery = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Reddit Links (Launch: {self.launch or 'N/A'})"


class FlickrLinks(models.Model):
    """
    Represents the 'flickr' nested object within 'links'.
    """
    small = models.JSONField(default=list, null=True, blank=True)
    original = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return f"Flickr Links ({len(self.original)} original images)"


class LaunchLinks(models.Model):
    """
    Represents the 'links' nested object within a Launch.
    """
    patch = models.ForeignKey(
        PatchLinks,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    reddit = models.ForeignKey(
        RedditLinks,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    flickr = models.ForeignKey(
        FlickrLinks,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    presskit = models.URLField(max_length=200, null=True, blank=True)
    webcast = models.URLField(max_length=200, null=True, blank=True)
    youtube_id = models.CharField(max_length=50, null=True, blank=True)
    article = models.URLField(max_length=200, null=True, blank=True)
    wikipedia = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Launch Links (YouTube ID: {self.youtube_id or 'N/A'})"


class LaunchCore(models.Model):
    """
    Represents a single core object within the 'cores' list of a Launch.
    """
    core = models.CharField(max_length=255, null=True, blank=True)
    flight = models.IntegerField(null=True, blank=True)
    gridfins = models.BooleanField(null=True, blank=True)
    legs = models.BooleanField(null=True, blank=True)
    reused = models.BooleanField(null=True, blank=True)
    landing_attempt = models.BooleanField(null=True, blank=True)
    landing_success = models.BooleanField(null=True, blank=True)
    landing_type = models.CharField(max_length=50, null=True, blank=True)
    landpad = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Core {self.core or 'N/A'} (Flight: {self.flight or 'N/A'})"


class Launch(models.Model):
    '''
    Represents a single launch
    '''
    launch_id = models.CharField(max_length=255)
    fairings = models.JSONField(null=True, blank=True)
    static_fire_date_utc = models.DateTimeField(null=True, blank=True)
    static_fire_date_unix = models.IntegerField(null=True, blank=True)
    tdb = models.BooleanField(null=True, blank=True)
    net = models.BooleanField(null=True, blank=True)
    window = models.IntegerField(null=True, blank=True)
    rocket = models.CharField(max_length=255, null=True, blank=True)
    success = models.BooleanField(null=True, blank=True)
    failures = models.JSONField(default=list, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    ships = models.JSONField(default=list, null=True, blank=True)
    capsules = models.JSONField(default=list, null=True, blank=True)
    launchpad = models.CharField(max_length=255, null=True, blank=True)
    auto_update = models.BooleanField(null=True, blank=True)
    flight_number = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    date_utc = models.DateTimeField(null=True, blank=True)
    date_unix = models.IntegerField(null=True, blank=True)
    date_local = models.DateTimeField(null=True, blank=True)
    date_precision = models.CharField(max_length=50, null=True, blank=True)
    upcoming = models.BooleanField(null=True, blank=True)

    # Nested objects as OneToOne or ManyToMany relationships
    links = models.OneToOneField(
        LaunchLinks,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    crew = models.ManyToManyField(
        CrewMember,
        blank=True
    )
    payloads = models.ManyToManyField(
        Payload,
        blank=True,
        related_name='launches'
    )
    cores = models.ManyToManyField(
        LaunchCore,
        blank=True
    )

    def __str__(self):
        return f"{self.name}"