using System.Web.Mvc;

namespace TallyUp.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            ViewBag.Message = "Social, real-time voting.";

            return View();
        }

        public ActionResult About()
        {
            ViewBag.Message = "Changing the way the world votes.";

            return View();
        }

        public ActionResult Contact()
        {
            return View();
        }
    }
}