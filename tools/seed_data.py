"""Data table for the second batch of manifests (plan f4e069bb phase 2).

Deliberately conservative on `install.type`: only apps with a real, currently
known Kodi addon get `kodi-repo`/`zip-url`; every DRM-locked or
addon-less streaming service gets `external-app` (informative listing only,
no automatic install in V1) rather than pointing at a source that would not
actually work. See docs note in README.md and CHANGELOG for the rationale.
"""

APPS = [
    # -- SVOD internationaux --
    dict(id="video.netflix", name="Netflix", category="svod",
         description="Films et series Netflix.",
         install=dict(type="external-app", source_url="https://www.netflix.com"),
         legal_notice=(
             "Necessite un abonnement Netflix actif. Aucun addon Kodi tiers "
             "ne fonctionne de maniere fiable face au DRM Widevine de "
             "Netflix (les tentatives passees type NetflixBMC sont "
             "abandonnees) -- fiche informative uniquement, pas "
             "d'installation automatique en V1. Aucun contenu redistribue "
             "par akasha-os-store.")),
    dict(id="video.disneyplus", name="Disney+", category="svod",
         description="Catalogue Disney, Pixar, Marvel, Star Wars, National Geographic.",
         install=dict(type="external-app", source_url="https://www.disneyplus.com"),
         legal_notice=(
             "Necessite un abonnement Disney+ actif. Pas d'addon Kodi "
             "fonctionnel connu (DRM). Fiche informative uniquement. Aucun "
             "contenu redistribue par akasha-os-store.")),
    dict(id="video.paramountplus", name="Paramount+", category="svod",
         description="Catalogue Paramount, series et films.",
         install=dict(type="external-app", source_url="https://www.paramountplus.com"),
         legal_notice=(
             "Necessite un abonnement Paramount+ actif. Pas d'addon Kodi "
             "fonctionnel connu. Fiche informative uniquement. Aucun "
             "contenu redistribue par akasha-os-store.")),
    dict(id="video.max", name="Max", category="svod",
         description="Catalogue Warner Bros. Discovery (ex-HBO Max).",
         install=dict(type="external-app", source_url="https://www.max.com"),
         legal_notice=(
             "Necessite un abonnement Max actif. Pas d'addon Kodi "
             "fonctionnel connu. Fiche informative uniquement. Aucun "
             "contenu redistribue par akasha-os-store.")),
    dict(id="video.crunchyroll", name="Crunchyroll", category="svod",
         description="Animes en simulcast et catalogue Crunchyroll.",
         install=dict(type="external-app", source_url="https://www.crunchyroll.com"),
         legal_notice=(
             "Necessite un abonnement Crunchyroll (un niveau gratuit avec "
             "publicite existe). D'anciens addons Kodi communautaires ont "
             "existe mais se sont casses a repetition suite aux "
             "changements d'API de Crunchyroll -- fiche informative "
             "uniquement pour eviter de pointer vers une source non "
             "maintenue. Aucun contenu redistribue par akasha-os-store.")),
    dict(id="video.appletvplus", name="Apple TV+", category="svod",
         description="Catalogue original Apple TV+.",
         install=dict(type="external-app", source_url="https://tv.apple.com"),
         legal_notice=(
             "Necessite un abonnement Apple TV+ actif. Pas d'addon Kodi "
             "fonctionnel connu (DRM FairPlay). Fiche informative "
             "uniquement. Aucun contenu redistribue par akasha-os-store.")),
    dict(id="video.discoveryplus", name="Discovery+", category="svod",
         description="Documentaires et catalogue Discovery.",
         install=dict(type="external-app", source_url="https://www.discoveryplus.com"),
         legal_notice=(
             "Necessite un abonnement Discovery+ actif. Pas d'addon Kodi "
             "fonctionnel connu. Fiche informative uniquement. Aucun "
             "contenu redistribue par akasha-os-store.")),
    dict(id="video.adn", name="ADN (Anime Digital Network)", category="svod",
         description="Animes en simulcast VOSTFR/VF, catalogue ADN.",
         install=dict(type="external-app", source_url="https://animedigitalnetwork.fr"),
         legal_notice=(
             "Necessite un abonnement ADN actif (un niveau gratuit avec "
             "publicite existe). Pas d'addon Kodi fonctionnel connu. Fiche "
             "informative uniquement. Aucun contenu redistribue par "
             "akasha-os-store.")),
    dict(id="video.ocs", name="OCS", category="svod",
         description="Cinema et series OCS (Orange).",
         install=dict(type="external-app", source_url="https://www.ocs.fr"),
         legal_notice=(
             "Necessite un abonnement OCS actif. La marque OCS a connu des "
             "evolutions recentes cote Orange -- verifier la disponibilite "
             "reelle du service au moment de l'installation. Pas d'addon "
             "Kodi fonctionnel connu. Fiche informative uniquement. Aucun "
             "contenu redistribue par akasha-os-store.")),
    dict(id="video.mubi", name="Mubi", category="svod",
         description="Cinema d'auteur et catalogue curate Mubi.",
         install=dict(type="external-app", source_url="https://mubi.com"),
         legal_notice=(
             "Necessite un abonnement Mubi actif. Pas d'addon Kodi "
             "fonctionnel connu. Fiche informative uniquement. Aucun "
             "contenu redistribue par akasha-os-store.")),

    # -- Replay France --
    dict(id="video.catchuptvandmore", name="Catch-up TV & More", category="replay",
         description=(
             "Agregateur communautaire de replay/direct pour de nombreuses "
             "chaines francaises et internationales (Arte, 6play, TF1, "
             "France Info, BFM TV, CNews, LCI, RMC, C8 et bien d'autres "
             "sont accessibles depuis cet unique addon)."),
         install=dict(
             type="kodi-repo",
             source_url=(
                 "https://github.com/Catch-up-TV-and-More/"
                 "plugin.video.catchuptvandmore"),
             addon_id="plugin.video.catchuptvandmore"),
         legal_notice=(
             "Addon communautaire tiers, non officiel. Chaque chaine reste "
             "soumise a ses propres conditions d'acces (geo-restriction "
             "France pour la plupart). Aucun contenu redistribue par "
             "akasha-os-store, l'addon ne fait que relayer les flux "
             "publics des chaines.")),
    dict(id="tv.arte", name="Arte", category="replay",
         description="Replay et direct Arte.",
         install=dict(type="external-app", source_url="https://www.arte.tv"),
         legal_notice=(
             "Contenu gratuit, geo-restreint France/Allemagne selon les "
             "programmes. Egalement accessible depuis l'addon Catch-up TV "
             "& More (voir video.catchuptvandmore) -- fiche independante "
             "conservee pour un acces direct depuis Mes Applications. "
             "Aucun contenu redistribue par akasha-os-store.")),
    dict(id="tv.6play", name="6play", category="replay",
         description="Replay et direct M6, W9, 6ter, Gulli.",
         install=dict(type="external-app", source_url="https://www.6play.fr"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. Egalement accessible "
             "depuis l'addon Catch-up TV & More. Aucun contenu redistribue "
             "par akasha-os-store.")),
    dict(id="tv.tf1plus", name="TF1+", category="replay",
         description="Replay et direct TF1, TMC, TFX, TF1 Series Films (ex-MyTF1).",
         install=dict(type="external-app", source_url="https://www.tf1.fr"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. Egalement accessible "
             "depuis l'addon Catch-up TV & More. Aucun contenu redistribue "
             "par akasha-os-store.")),
    dict(id="tv.franceinfo", name="France Info (replay)", category="replay",
         description="Replay des magazines et journaux franceinfo.",
         install=dict(type="external-app", source_url="https://www.francetvinfo.fr"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. France Info fait "
             "partie du groupe France Televisions -- egalement accessible "
             "via l'addon france.tv (tv.francetv) ou Catch-up TV & More. "
             "Aucun contenu redistribue par akasha-os-store.")),
    dict(id="tv.bfmtv", name="BFM TV (replay)", category="replay",
         description="Replay des journaux et magazines BFM TV.",
         install=dict(type="external-app", source_url="https://www.bfmtv.com"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. Egalement accessible "
             "depuis l'addon Catch-up TV & More. Aucun contenu redistribue "
             "par akasha-os-store.")),
    dict(id="tv.cnews", name="CNews (replay)", category="replay",
         description="Replay des journaux et magazines CNews.",
         install=dict(type="external-app", source_url="https://www.cnews.fr"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. Egalement accessible "
             "depuis l'addon Catch-up TV & More. Aucun contenu redistribue "
             "par akasha-os-store.")),
    dict(id="tv.lci", name="LCI (replay)", category="replay",
         description="Replay des journaux et magazines LCI.",
         install=dict(type="external-app", source_url="https://www.lci.fr"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. Egalement accessible "
             "depuis l'addon Catch-up TV & More. Aucun contenu redistribue "
             "par akasha-os-store.")),
    dict(id="tv.rmcstory", name="RMC Story / RMC Decouverte", category="replay",
         description="Replay RMC Story et RMC Decouverte.",
         install=dict(type="external-app", source_url="https://rmcstory.bfmtv.com"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. Egalement accessible "
             "depuis l'addon Catch-up TV & More. Aucun contenu redistribue "
             "par akasha-os-store.")),
    dict(id="tv.c8", name="C8 (replay)", category="replay",
         description="Replay des programmes C8.",
         install=dict(type="external-app", source_url="https://www.c8.fr"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. Egalement accessible "
             "depuis l'addon Catch-up TV & More. Aucun contenu redistribue "
             "par akasha-os-store.")),

    # -- TV en direct gratuite --
    dict(id="video.rakuten", name="Rakuten TV", category="live-tv",
         description="Chaines gratuites en direct et location de films Rakuten TV.",
         install=dict(type="external-app", source_url="https://www.rakuten.tv"),
         legal_notice=(
             "Chaines FAST gratuites avec publicite ; les locations/achats "
             "de films necessitent un compte Rakuten TV. Pas d'addon Kodi "
             "fonctionnel connu. Fiche informative uniquement. Aucun "
             "contenu redistribue par akasha-os-store.")),
    dict(id="tv.france24", name="France 24 Live", category="live-tv",
         description="Direct continu d'information internationale France 24.",
         install=dict(type="external-app", source_url="https://www.france24.com/fr/direct/"),
         legal_notice=(
             "Flux gratuit et non geo-restreint. Pas d'addon Kodi dedie "
             "activement maintenu identifie -- fiche informative "
             "uniquement en V1. Aucun contenu redistribue par "
             "akasha-os-store.")),
    dict(id="tv.euronews", name="Euronews", category="live-tv",
         description="Direct continu d'information europeenne Euronews.",
         install=dict(type="external-app", source_url="https://www.euronews.com/live"),
         legal_notice=(
             "Flux gratuit et non geo-restreint. Pas d'addon Kodi dedie "
             "activement maintenu identifie -- fiche informative "
             "uniquement en V1. Aucun contenu redistribue par "
             "akasha-os-store.")),
    dict(id="tv.tf1info", name="TF1 Info", category="live-tv",
         description="Direct continu d'information TF1 Info.",
         install=dict(type="external-app", source_url="https://www.tf1info.fr/direct/"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. Pas d'addon Kodi dedie "
             "identifie -- fiche informative uniquement en V1. Aucun "
             "contenu redistribue par akasha-os-store.")),
    dict(id="tv.bfmlive", name="BFM Live", category="live-tv",
         description="Direct continu d'information BFM TV.",
         install=dict(type="external-app", source_url="https://www.bfmtv.com/en-direct/"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. Distinct de la fiche "
             "replay tv.bfmtv (memes conditions). Pas d'addon Kodi dedie "
             "identifie -- fiche informative uniquement en V1. Aucun "
             "contenu redistribue par akasha-os-store.")),
    dict(id="tv.franceinfodirect", name="franceinfo: (direct continu)", category="live-tv",
         description="Direct continu d'information franceinfo:.",
         install=dict(type="external-app", source_url="https://www.francetvinfo.fr/en-direct/tv.html"),
         legal_notice=(
             "Contenu gratuit geo-restreint France. Distinct de la fiche "
             "replay tv.franceinfo (memes conditions, flux different). "
             "Egalement accessible via l'addon france.tv (tv.francetv). "
             "Aucun contenu redistribue par akasha-os-store.")),

    # -- Sport --
    dict(id="sport.dazn", name="DAZN", category="sport",
         description="Sport a la demande et en direct DAZN.",
         install=dict(type="external-app", source_url="https://www.dazn.com"),
         legal_notice=(
             "Necessite un abonnement DAZN actif. Pas d'addon Kodi "
             "fonctionnel connu (DRM). Fiche informative uniquement. "
             "Aucun contenu redistribue par akasha-os-store.")),
    dict(id="sport.lequipe", name="L'Equipe", category="sport",
         description="Actualite sportive et direct L'Equipe.",
         install=dict(type="external-app", source_url="https://www.lequipe.fr"),
         legal_notice=(
             "Contenu en grande partie gratuit, geo-restreint France pour "
             "certains directs. Pas d'addon Kodi dedie activement "
             "maintenu identifie -- fiche informative uniquement en V1. "
             "Aucun contenu redistribue par akasha-os-store.")),
    dict(id="sport.beinsports", name="beIN Sports Connect", category="sport",
         description="Sport en direct et a la demande beIN Sports.",
         install=dict(type="external-app", source_url="https://www.beinsports.com"),
         legal_notice=(
             "Necessite un abonnement beIN Sports actif. Pas d'addon Kodi "
             "fonctionnel connu. Fiche informative uniquement. Aucun "
             "contenu redistribue par akasha-os-store.")),
    dict(id="sport.eurosport", name="Eurosport", category="sport",
         description="Sport en direct et a la demande Eurosport / max (Discovery).",
         install=dict(type="external-app", source_url="https://www.eurosport.fr"),
         legal_notice=(
             "Necessite un abonnement Eurosport actif pour la plupart des "
             "contenus. Pas d'addon Kodi fonctionnel connu. Fiche "
             "informative uniquement. Aucun contenu redistribue par "
             "akasha-os-store.")),
    dict(id="sport.ligue1plus", name="Ligue 1+", category="sport",
         description="Diffuseur officiel de la Ligue 1 (LFP).",
         install=dict(type="external-app", source_url="https://www.ligue1plus.fr"),
         legal_notice=(
             "Necessite un abonnement Ligue 1+ actif. Service recent "
             "(lance par la LFP en 2024) -- pas d'addon Kodi fonctionnel "
             "connu. Fiche informative uniquement. Aucun contenu "
             "redistribue par akasha-os-store.")),

    # -- Musique --
    dict(id="musique.spotify", name="Spotify", category="musique",
         description="Streaming musical Spotify.",
         install=dict(type="external-app", source_url="https://www.spotify.com"),
         legal_notice=(
             "Necessite un compte Spotify (gratuit avec publicite ou "
             "Premium). Pas d'addon Kodi natif fiable -- Spotify Connect "
             "(cast depuis un telephone) reste la meilleure integration "
             "pratique sur ce type d'appareil, hors perimetre "
             "d'installation automatique V1. Aucun contenu redistribue "
             "par akasha-os-store.")),
    dict(id="musique.deezer", name="Deezer", category="musique",
         description="Streaming musical Deezer.",
         install=dict(type="external-app", source_url="https://www.deezer.com"),
         legal_notice=(
             "Necessite un compte Deezer (gratuit avec publicite ou "
             "Premium). Pas d'addon Kodi fonctionnel connu. Fiche "
             "informative uniquement. Aucun contenu redistribue par "
             "akasha-os-store.")),
    dict(id="musique.applemusic", name="Apple Music", category="musique",
         description="Streaming musical Apple Music.",
         install=dict(type="external-app", source_url="https://music.apple.com"),
         legal_notice=(
             "Necessite un abonnement Apple Music actif. Pas d'addon Kodi "
             "fonctionnel connu. Fiche informative uniquement. Aucun "
             "contenu redistribue par akasha-os-store.")),
    dict(id="musique.youtubemusic", name="YouTube Music", category="musique",
         description="Streaming musical YouTube Music.",
         install=dict(
             type="kodi-repo",
             source_url="https://mirrors.kodi.tv/addons/omega/",
             addon_id="plugin.video.youtube"),
         legal_notice=(
             "Utilise le meme addon officiel que YouTube (plugin.video."
             "youtube, deja utilise ailleurs dans Akasha OS pour les "
             "Comptes & Services) -- la recherche/lecture de musique "
             "fonctionne mais l'interface n'est pas dediee musique comme "
             "l'app native. Necessite un compte Google pour certains "
             "contenus. Aucun contenu redistribue par akasha-os-store.")),
    dict(id="musique.amazonmusic", name="Amazon Music Unlimited", category="musique",
         description="Streaming musical Amazon Music.",
         install=dict(type="external-app", source_url="https://music.amazon.fr"),
         legal_notice=(
             "Necessite un abonnement Amazon Music actif. Pas d'addon "
             "Kodi fonctionnel connu. Fiche informative uniquement. "
             "Aucun contenu redistribue par akasha-os-store.")),
]
