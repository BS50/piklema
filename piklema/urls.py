from piklema.views.device_views import DeviceModelView
from piklema.views.tag_value_views import TagValueModelView
from piklema.views.tag_views import TagModelView
from piklema.views.user_views import UserModelView
from dotenv import load_dotenv
from rest_framework.routers import SimpleRouter

load_dotenv()

router = SimpleRouter()
router.register("user", UserModelView, "user")
router.register("device", DeviceModelView, "device")
router.register("tag", TagModelView, "tag")
router.register("tag_value", TagValueModelView, "tag-value")

urlpatterns = router.urls
