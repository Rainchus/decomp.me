from django.urls import path

from coreapp.views import (
    compilers,
    libraries,
    platform,
    preset,
    stats,
    project,
    scratch,
    user,
)

urlpatterns = [
    path("compilers", compilers.CompilersDetail.as_view(), name="compilers"),
    path("libraries", libraries.LibrariesDetail.as_view(), name="libraries"),
    path("platform", platform.PlatformDetail.as_view(), name="platform"),
    path(
        "platform/<slug:id>",
        platform.single_platform,
        name="platform-detail",
    ),
    path("stats", stats.StatsDetail.as_view(), name="stats"),
    *scratch.router.urls,
    *preset.router.urls,
    *project.router.urls,
    path("user", user.CurrentUser.as_view(), name="current-user"),
    path(
        "user/scratches",
        user.CurrentUserScratchList.as_view(),
        name="current-user-scratches",
    ),
    path("users/<slug:username>", user.user, name="user-detail"),
    path(
        "users/<slug:username>/scratches",
        user.UserScratchList.as_view(),
        name="user-scratches",
    ),
]
