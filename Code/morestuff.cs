using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using MendTicketMast.Helpers;

namespace MendTicketMast
{
    public static class CreateIncident
    {
        [FunctionName("CreateIncident")]
        public static async Task<IActionResult> Run([HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req, ILogger log)
        {
            #region getInputs
            string messaging = "";
            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            string description = req.Query["Description"];
            string shortDescription = req.Query["ShortDescription"];
            string assignmentGroup = req.Query["AssignmentGroup"];
            string impact = req.Query["Impact"];
            string urgency = req.Query["Urgency"];

            dynamic data = JsonConvert.DeserializeObject(requestBody);

            description = description ?? data?.Description;
            if (string.IsNullOrEmpty(description))
                messaging += "Description cannot be null.";
            shortDescription = shortDescription ?? data?.ShortDescription;
            if (string.IsNullOrEmpty(shortDescription))
                messaging += "ShortDescription cannot be null.";
            assignmentGroup = assignmentGroup ?? data?.AssignmentGroup;
            if (string.IsNullOrEmpty(assignmentGroup))
                messaging += "AssignmentGroup cannot be null.";
            if (string.IsNullOrEmpty(assignmentGroup))
                messaging += "Must include an assignment group";
            else if (assignmentGroup.ToLower().StartsWith("SD_"))
                messaging += "AssignmentGroup must start with SD_.";
            impact = impact ?? data?.Impact;
            if (string.IsNullOrEmpty(impact))
                impact = "3";
            urgency = urgency ?? data?.Urgency;
            if (string.IsNullOrEmpty(urgency))
                urgency = "3";
            #endregion
            if (string.IsNullOrEmpty(messaging))
            {
                ServiceNow sn = new ServiceNow();
                var output = sn.CreateIncident(description, shortDescription, assignmentGroup, impact, urgency, log);
                output.Wait();
                return new OkObjectResult(output.Result);
            }
            else
            {
                BadRequestObjectResult br = new BadRequestObjectResult(messaging);
                br.StatusCode = 500;
                return br;
            }
        }
    }
}
