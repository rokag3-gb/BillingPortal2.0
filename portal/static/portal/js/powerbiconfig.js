// Read embed application token from textbox
var txtAccessToken = "H4sIAAAAAAAEAB2WR6rFCpJE9_KnKpDXlQpqIO-910zee6-m996va5xBQh4iififf6z0Hea0-Off__CXz7Gp5VEtNlBE17HZ6jEVMVdvlGGnaBOPwzWLWd9tMTd8olg_vC6Axe2e5wKI3uwYmi6_aKwtmEYzXxwlkVR0y6JegXACKAXDNfmcfmj3-gB1Yq9_6Zj2ZGyse2PuZpk3Z9wvGZvyXosqOaCFjjJNatwDMcD0IMNylBokq-y59GVFWQtOVVfA7Y0cOTRVOF7G_sQcZAvWkcWJ7gHchvdOCB54qiNE_ho9YYR8dODbKnyNQHkPZk3Eaow1vkHhg_bhx_Syha9352t3b-C_LFfqFhevVuDPOhorl7T9NmH9tvF67e3Bj9I-Iz4YuDtI29YYR2UNBJOwEHoGTIm_i_MXfhpcEROk_I31nxU7vjIcFBfwkAzXDRfUzfhs9qMklZ-fpI0o5FJTiJ-AtL9q1HWZyBLNzis1FI7RkwOaRWjQRXK88ipNXnlN2H6r2rDY1y5gOVV4-9AqqDefcitt9dBVPdhkzlrNi-HIyQdmjo3it3kNS75Q0wlE6xh4BJ8maH7Q_C_Dkh56yN4Lydy5j5ieIjx-1TJzYEMb2N9NC7myOPDhSYNRjP2yCrDXU7-_E92XGF-330qS8zJtNXzK86WuztXpuUbl6HdLrgX6ODxhPNighq7zexFX_ryU-8KRx2HcA5LmT47mHOMwq_3yrpFEQZc_aH8WXONsMjaWdn35mb9TiiCfb3fjqIMeGeEb_Yx_BFyWZcP4NNkdy9UwmtBCx8dgd0QXVrdAtQzpxmN3wnmG6mbUmdGISOSpUsRyDpiFRuvoTzfSsBDEVypqHRuYD0p18wnz3a5hsxxh3cGck0w0bjkd9hqmnG1JEfSw_DMQmBkQYeOvvPA74x3JTIa4m0kUf4PoGlrI-Sfot-5BCROsWGGVoFU-Kw1pv9C4aH1eFbPkwppR20V8Zck7bmN85PuHirVOB8dF1GjrHzUlhizd5HD97Kmp6XipdqIWI2WN8RRuJwNedKilDbpI7Oe-54y89CBkYeBpLhToMdBmR7LNbTgsypJjQKaCFjIvDxEGVr3qhFxeVSG8LcPEblNi5VgN8pOtQkzg5gwxAEpCP_x-CHUwyHjQxTIuPjbRzmBxToX9btHxq82mOZUUSsz693cvEYr43BYF0zN7qxIRQzGglDAK77PZYn00C1D6-pt1JcFmmordXHBVNi_auptNQ7OVVt-nzKVrR7faPnTgPOQI0EszKli6WUL89M9cpVmMnkw-PJFroC_WmdV2AoKeulGx65-eLuCQoDh9faydEI2QuQar4pKiNT2DQcpdvw8B2xTOPUhYpPLnjQLxllL2S00kyDtbxt6uxODNAsE_rwR0UTVwVCT-xdNk8FVTiqz1FdJ1eSCQ6dIegOeXVsNKrlgCbDiFhe6ieUC-fGcpFygXpXn0l_NnqbX1GBswfqHdmdg5QfyQ8MKlm-Ypj823Oz1pk50cxfx2QJU2XNbvdtnkB2ji6hmNP3-DB7eNM4uBcReMKbdD_kisZq31eKlYBo9NFW8ILFMzYvHsV1eGnwo6vyycTpCvn4ThTfrPxz0lF28gUIhl3hv0QZLyQLmMBkISSpeuPUJzaA6FgvYC7Dm8JWdtbwWpeAHQArTSnxaoNs8wJNdm6e0P9CBzGCGhFKeMM-E5AVGTVCeG78M9L6Ct1fyTN6zpJ_uYxi1ir38grlK5hVCQH125co9aXUzv-WWyqqJETX0DT37aOg_QVST2TO4AaHd1WMfKiDFmHCuQdaFEFaSAeF4y9YcbAZFyPLgOBjjXJqLw1AgwAJ9JHzTZ0-83otXIoZZkI7vAuIMrHcvwxbhGjH8gcr11t5K8Dmyzi-0GpoC3m-8tfEo2m4vu7rmllVit64QQImZjkqOJuw0RT_6GjoU_3sZzNoxF8wcaa0UoRv6s1SoiB-T5TgPybw8gt1QNi8HjcoEfgMix9HImeJEUi-LSeJPVC6UwLVbypHJ2DWs6eBRKK-w3PqIEp0Q8NiqOqXIzVWCobvrJqUIx0QSTxy37zYF_1oTZE8Ah79xnpTtv6JMJwxHl90ZSzHq3dSqborNUA9e9ixRQM4ZnZ4GAKr31aTyjXWKeKGUvbi7-7VRm4yQp2lBsxM0MwE8aTOYeviLX-LhnSIfHc6Bk4dtziT4l7BuSgy-kpR1zNxBRIW34IRJiFfX31idB3CSgsql4zP6mwyrH2uBVs0qee_eMYWqy2BJzIZXTCD4AfsWADtFZdRIUjH7pKAvqy0PBHRgLX6T_kmvWu4YBwGWnELe3cPjsUaHjW3BzHg3sqeomAulisI6w2uZdqB0e4fV3shUmLtoaToSl7k1_yqanI3-9AAkTQD4soTHcAMQ63tsj5fP5vV0pSQsDb0Km5eXfc8EFkjhiOxbn1LwtIrJx0nuYi8iOWfQciQzLGAHyWGknHkqidPyNC3FKIWPX__nnX_-w27scs1q-f9VLpnWnTZzMK-dTNDGRXAtYGrof7l6CTignLuf73fIDGxPwvoM0adutjOhnzrYgqGVEvtOeyKAuMjRYqF5pWdi6liz0mhnxKR5NEcpKgdAqa19cZGabvLpgU648YB2AiXpK6-ZU5IFp1md8hKVRFwM6B9X-2wCKJBjLA53uEID0X5oUgoFyLllhPbmjKaV_OBDKv1sDI5wpnQGmPicmHOyHqG4lcbx8p4fzYSPJnSaqqWMi9fe5YSGcomkykHhaBBFQAqT4My9MGaRbIHh7WWMdnWh3Wv7SwhM2Kdf4np_yac1LIQnmvSV-hS21JrcQ91wel7H3BDjvAg8OxtmbUWPYDGj_57-Y36UpNzn4o8wUpnvbMFS6MrXhmYdhsrHd_1W5bT2lx7mVfzIHPJOdV8SrNG4zoKYJSpuQEGF_ApP2a4CANw6nGlzFK9bpvieM8Nv8kpBKXG3UzU4qm6W3H-GFDh32nYqH_S2IYk0AP3xidiGm9X7rgNJJhKiKFirAFjTTufOCBVpeh2qz7w9HnWM0VMk-4q5GLP5c7juhv78kWUYKLbh27m--oHGIq3U7D-SVC1Iof3JXYYQaPnW9Liyri9E8v8zTcOl-YpqD7MZfWeod8BtwQ_JL6C0c_7vWP978FMgl7G2B3q0P-dcRaB90Kxwmia1Usza6gPyqnlwyxyN5O3X5TZxzfHsM5ig80Cg0euyWe-z-9depFuizuB-LcoAbqdyvbQMaHf8f8__-H2BKgwRuDAAA.eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVVTLU5PUlRILUNFTlRSQUwtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQiLCJlbWJlZEZlYXR1cmVzIjp7Im1vZGVybkVtYmVkIjpmYWxzZX19"

// Read embed URL from textbox
var txtEmbedUrl = "https://app.powerbi.com/reportEmbed?reportId=f6bfd646-b718-44dc-a378-b73e6b528204&groupId=be8908da-da25-452e-b220-163f52476cdd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVVTLU5PUlRILUNFTlRSQUwtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQiLCJlbWJlZEZlYXR1cmVzIjp7Im1vZGVybkVtYmVkIjp0cnVlfX0%3d"

// Read report Id from textbox
var txtEmbedReportId = "f6bfd646-b718-44dc-a378-b73e6b528204"

// Read embed type from radio
var tokenType = $('input:radio[name=tokenType]:checked').val();

// Get models. models contains enums that can be used.
var models = window['powerbi-client'].models;

// Embed configuration used to describe the what and how to embed.
// This object is used when calling powerbi.embed.
// This also includes settings and options such as filters.
// You can find more information at https://github.com/Microsoft/PowerBI-JavaScript/wiki/Embed-Configuration-Details.
var config = {
    type: 'report',
    tokenType: models.TokenType.Embed,
    accessToken: txtAccessToken,
    embedUrl: txtEmbedUrl,
    id: txtEmbedReportId,
    permissions: models.Permissions.All /*gives maximum permissions*/,
    // viewMode: models.ViewMode.Edit,
    settings: {
        background: models.BackgroundType.Transparent,
        filterPaneEnabled: false,
        navContentPaneEnabled: false,
        bars:{
			actionBar: {
				visible: false
			}
		},
		panes:{
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
				visible: true
			},
			syncSlicers: {
				visible: true
			},
			visualizations: {
				expanded: true
			}
		}
	}
};

// Get a reference to the embedded report HTML element
var embedContainer = $('#embedContainer')[0];

// Embed the report and display it within the div container.
var report = powerbi.embed(embedContainer, config);

// Report.off removes a given event handler if it exists.
report.off("loaded");

// Report.on will add an event handler which prints to Log window.
report.on("loaded", function () {
    Log.logText("Loaded");
});

// Report.off removes a given event handler if it exists.
report.off("rendered");

// Report.on will add an event handler which prints to Log window.
report.on("rendered", function () {
    Log.logText("Rendered");
});

report.off("error");
report.on("error", function (event) {
    Log.log(event.detail);
});

report.off("saved");
report.on("saved", function (event) {
    Log.log(event.detail);
    if (event.detail.saveAs) {
        Log.logText('In order to interact with the new report, create a new token and load the new report');
    }
});
