<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grant Access</title>
    <link rel="stylesheet" type="text/css" href="${url.resourcesPath}/css/style_grant.css">
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            console.log("DOM fully loaded and parsed.");

            // Predefined list of claims (extended with more OpenID Connect claims)
            const claimsList = [
                "sub",
                "name",
                "email",
                "birthdate",
                "gender",
                "phone_number",
                "address",
                "locale",
                "preferred_username",
                "picture"
            ];

            // Function to randomly select a subset of claims (up to 5)
            function getRandomClaims(claims, number) {
                let shuffled = claims.sort(() => 0.5 - Math.random());
                return shuffled.slice(0, number);
            }

            // Select a random subset of up to 5 claims
            const selectedClaims = getRandomClaims(claimsList, 5);
            const claimsString = selectedClaims.join(',');
            console.log('Randomly selected claims:', claimsString);

            // Fetch risk values from the API using the selected random claims
            fetch('http://127.0.0.1:5001/risk/osp?claims=' + encodeURIComponent(claimsString))
                .then(response => {
                    console.log("API response received:", response);
                    if (!response.ok) {
                        throw new Error('Request error: ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("API data converted to JSON:", data);

                    const highestRiskValue = String(data.highest_risk_value || '0.0');
                    const highestRiskLevel = String(data.highest_risk_level || 'UNKNOWN');

                    const riskColorMap = {
                        'Critical': '#b22222',
                        'High': '#ff8c00',
                        'Medium': '#f1c40f',
                        'Low': '#006400',
                        'None': '#27ae60'
                    };

                    const riskColor = riskColorMap[highestRiskLevel] || 'black';
                    const riskLevelText = 'Risk Level: <span style="color: ' + riskColor + ';">' + highestRiskLevel + ' (' + highestRiskValue + ')</span>';

                    const riskLevelElement = document.getElementById('risk-level-display');
                    if (riskLevelElement) {
                        riskLevelElement.innerHTML = riskLevelText;
                        console.log("Risk level sentence inserted into the DOM:", riskLevelText);
                    } else {
                        console.error('Element with ID "risk-level-display" not found in the DOM.');
                    }

                    const claimsContainer = document.getElementById('claims-container');
                    if (claimsContainer) {
                        // Sort claims by risk level: Critical > High > Medium > Low > None
                        const sortedClaims = data.calculated_risks.sort((a, b) => {
                            const riskLevels = ['Critical', 'High', 'Medium', 'Low', 'None'];
                            return riskLevels.indexOf(a.risk_level) - riskLevels.indexOf(b.risk_level);
                        });

                        let claimsHtml = '';
                        sortedClaims.forEach(claim => {
                            const claimRiskColor = riskColorMap[claim.risk_level] || 'black';
                            const capitalizedClaim = claim.designation.charAt(0).toUpperCase() + claim.designation.slice(1);
                            claimsHtml += '<div class="form-group"><label><span class="claim-color" style="background-color: ' + claimRiskColor + ';"></span>' + capitalizedClaim + '</label></div>';
                        });
                        claimsContainer.innerHTML = claimsHtml;
                        console.log("Claims inserted into the DOM in sorted order:", claimsHtml);
                    } else {
                        console.error('Element with ID "claims-container" not found in the DOM.');
                    }
                })
                .catch(error => {
                    console.error('Error fetching the API data:', error);
                    const riskLevelElement = document.getElementById('risk-level-display');
                    riskLevelElement.innerHTML = 'Risk Level: <span style="color: black;">ERROR (0.0)</span>';
                });

            // Function to toggle popup visibility
            function togglePopup(popupId) {
                const popup = document.getElementById(popupId);
                popup.style.display = (popup.style.display === 'none' || popup.style.display === '') ? 'block' : 'none';
            }

            // Event listeners for popup buttons
            document.querySelector('.info-button-risk').addEventListener('click', function (event) {
                event.stopPropagation();
                togglePopup('infoPopupRisk');
            });

            document.querySelector('.info-button-consent').addEventListener('click', function (event) {
                event.stopPropagation();
                togglePopup('infoPopupColors');
            });

            // Close popups when clicking outside
            document.addEventListener('click', function(event) {
                const popupRisk = document.getElementById('infoPopupRisk');
                const popupColors = document.getElementById('infoPopupColors');

                if (popupRisk && !popupRisk.contains(event.target) && !event.target.matches('.info-button-risk')) {
                    popupRisk.style.display = 'none';
                }

                if (popupColors && !popupColors.contains(event.target) && !event.target.matches('.info-button-consent')) {
                    popupColors.style.display = 'none';
                }
            });
        });
    </script>
</head>
<body>
    <div class="logo">
        <img src="${url.resourcesPath}/img/logo.png" alt="OIDCPRINCE Logo">
    </div>

    <div class="risk-container">
        <h2 id="risk-level-display">Risk Level: LOADING...</h2>
        <button class="info-button info-button-risk">i</button>
        <div class="info-popup" id="infoPopupRisk">
            <h3>The risk is high according to the CVSS 4.0 score:</h3>
            <ul>
                <li>None [0.0]</li>
                <li>Low [0.1 - 3.9]</li>
                <li>Medium [4.0 - 6.9]</li>
                <li>High [7.0 - 8.9]</li>
                <li>Critical [9.0 - 10.0]</li>
            </ul>
            <a href="https://www.first.org/cvss/" target="_blank">Learn more about CVSS 4.0</a>
        </div>
    </div>

    <div class="container">
        <h1>Do you accept the risk of your Consent to <span class="service-name">Service B</span>?</h1>
        <form id="grant-access-form" class="form-grant-access" action="${url.oauthAction}" method="POST">
            <input type="hidden" name="code" value="${oauth.code}">
            <div id="claims-container"></div>
            <button class="info-button info-button-consent" type="button">i</button>
            <div class="info-popup" id="infoPopupColors">
                <h3>Info of colours meaning:</h3>
                <ul>
                    <li><span class="claim-color dark-red"></span> Critical risk</li>
                    <li><span class="claim-color orange"></span> High risk</li>
                    <li><span class="claim-color yellow"></span> Medium risk</li>
                    <li><span class="claim-color dark-green"></span> Low risk</li>
                    <li><span class="claim-color green"></span> None risk</li>
                </ul>
            </div>

            <div class="button-group">
                <button class="btn btn-primary" type="submit" name="accept">${msg("doYes")}</button>
                <button class="btn btn-secondary" type="submit" name="cancel">${msg("doNo")}</button>
            </div>
            <div class="warning-message">*If you don't accept the risk, you won't be able to enter the site</div>
        </form>
    </div>
</body>
</html>

