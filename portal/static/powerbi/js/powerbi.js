// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

window.onload = function () {
    let reportContainer = document.getElementById("pbi-report-container");
    let errorContainer = document.getElementById("pbi-error-container");
    // Initialize iframe for embedding report
    powerbi.bootstrap(reportContainer, { type: "report" });

    var models = window["powerbi-client"].models;
    var reportLoadConfig = {
        type: "report",
        tokenType: models.TokenType.Embed,

        // Enable this setting to remove gray shoulders from embedded report
        settings: {
            background: models.BackgroundType.Transparent,
            bars: {
                actionBar: {
                    visible: false
                }
            },
            panes: {
                bookmarks: {
                    visible: false
                },
                fields: {
                    expanded: false
                },
                filters: {
                    expanded: false,
                    visible: false
                },
                pageNavigation: {
                    visible: false
                },
                selection: {
                    visible: false
                },
                syncSlicers: {
                    visible: true
                },
                visualizations: {
                    expanded: false
                }
            }
        }
    };

    fetch("/powerbi/token")
        .then(function (response) {
            return response.json();
        })
        .then(function (embedData) {
            reportLoadConfig.accessToken = embedData.accessToken;

            // You can embed different reports as per your need
            reportLoadConfig.embedUrl = embedData.reportConfig[0].embedUrl;

            // Use the token expiry to regenerate Embed token for seamless end user experience
            // Refer https://aka.ms/RefreshEmbedToken
            tokenExpiry = embedData.tokenExpiry;

            // Embed Power BI report when Access token and Embed URL are available
            var report = powerbi.embed(reportContainer, reportLoadConfig);

            // Triggers when a report schema is successfully loaded
            report.on("loaded", function () {
                console.log("Report load successful")
            });

            // Triggers when a report is successfully embedded in UI
            report.on("rendered", function () {
                console.log("Report render successful")
            });

            // Clear any other error handler event
            report.off("error");

            // Below patch of code is for handling errors that occur during embedding
            report.on("error", function (event) {
                var errorMsg = event.detail;

                // Use errorMsg variable to log error in any destination of choice
                console.error(errorMsg);
                return;
            });
        })
        .catch(function (error) {
            // Show error container
            reportContainer.hide();
            errorContainer.show();

            // Format error message
            // var errMessageHtml = "<strong> Error Details: </strong> <br/>" + $.parseJSON(error.responseText)["errorMsg"];
            // errMessageHtml = errMessageHtml.split("\n").join("<br/>")

            // Show error message on UI
            errorContainer.html("리포트 로드 중 오류 발생");
        });

}