// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
// Desktop >= 990px
var models = window["powerbi-client"].models;
window.onload = function () {
    let reportContainer = document.getElementById("pbi-report-container");
    let errorContainer = document.getElementById("pbi-error-container");
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const menuId = urlParams.get('menu_id');
    // console.log(urlParams.get('menu_id'));

    // Initialize iframe for embedding report
    

    var reportLoadConfig = {
        type: "report",
        embedUrl: 'https://app.powerbi.com/reportEmbed',
        tokenType: models.TokenType.Embed,
        // Enable this setting to remove gray shoulders from embedded report
        settings: {
            layoutType: models.LayoutType.MobilePortrait,
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
        },
        // filters: [hiddenBasicFilter]
    };
    powerbi.bootstrap(reportContainer, reportLoadConfig);
    let token_url = null;
    if (menuId){
        token_url = "/powerbi/token" + "?id=" + menuId
    }else{
        token_url = "/powerbi/token"
    }
    fetch(token_url)
        .then(function (response) {
            return response.json();
        })
        .then(function (embedData) {
            reportLoadConfig.accessToken = embedData.token.accessToken;
            reportLoadConfig.filters = [embedData.filter];

            // You can embed different reports as per your need
            reportLoadConfig.embedUrl = embedData.token.reportConfig[0].embedUrl;

            // Use the token expiry to regenerate Embed token for seamless end user experience
            // Refer https://aka.ms/RefreshEmbedToken
            tokenExpiry = embedData.token.tokenExpiry;

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

            // report.setFilters([hiddenBasicFilter])
            //     .catch(errors => {
            //         // Handle error
            //         console.log(errors)
            //     });
            setInterval(function () {
                report.refresh()
                    .catch(error => {
                        // Refresh error
                    });
            }, 1000 * 30);

            setInterval(function () {
                console.log("Token refreshing...")
                fetch("/powerbi/token")
                    .then(function (response) {
                        return response.json();
                    })
                    .then(function (json) {
                        report.setAccessToken(json.accessToken)
                            .then(function () {
                                console.log("Token refreshed")
                            })
                    })
            }, 1000 * 60 * 50);

            // Convert to mobile or desktop layout with media query event
            const mediaQueryList = window.matchMedia("(min-width: 992px)");
            let newLayout = mediaQueryList.matches? models.LayoutType.MobileLandscape : models.LayoutType.MobilePortrait
            const newSettings = { layoutType: newLayout };
            report.updateSettings(newSettings)
            mediaQueryList.addListener(function(event){
                console.log(event.matches? "Desktop":"Mobile");
                let newLayout = event.matches? models.LayoutType.MobileLandscape : models.LayoutType.MobilePortrait
                const newSettings = { layoutType: newLayout };
                report.updateSettings(newSettings)
                .then(async result => {
                    let pages = await report.getPages();
                    let layoutResult = await pages[0].hasLayout(newLayout);
                    console.log("Layout updated: "+layoutResult);
                })
                .catch(error => { 
                    console.log(error)
                 });;
                
            });
        })
        .catch(function (error) {
            console.log(error);
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