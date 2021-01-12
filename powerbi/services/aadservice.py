# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from flask import current_app as app
from django.conf import settings
import msal

class AadService:

    def get_access_token():
        '''Generates and returns Access token

        Returns:
            string: Access token
        '''
        powerbi_config = getattr(settings, "POWERBI", {})
        response = None
        try:
            if powerbi_config['AUTHMODE'].lower() == 'masteruser':

                # Create a public client to authorize the app with the AAD app
                clientapp = msal.PublicClientApplication(powerbi_config['CLIENT_ID'], authority=powerbi_config['AUTHORITY'])
                accounts = clientapp.get_accounts(username=powerbi_config['MASTER_USER'])

                if accounts:
                    # Retrieve Access token from user cache if available
                    response = clientapp.acquire_token_silent(powerbi_config['SCOPE'], account=accounts[0])

                if not response:
                    # Make a client call if Access token is not available in cache
                    response = clientapp.acquire_token_by_username_password(powerbi_config['MASTER_USER'], powerbi_config['MASTER_PASS'], scopes=powerbi_config['SCOPE'])     

            # Service Principal auth is the recommended by Microsoft to achieve App Owns Data Power BI embedding
            elif powerbi_config['AUTHMODE'].lower() == 'serviceprincipal':
                authority = powerbi_config['AUTHORITY'].replace('organizations', powerbi_config['TENANT_ID'])
                clientapp = msal.ConfidentialClientApplication(powerbi_config['CLIENT_ID'], client_credential=powerbi_config['CLIENT_SECRET'], authority=authority)

                # Make a client call if Access token is not available in cache
                response = clientapp.acquire_token_for_client(scopes=powerbi_config['SCOPE'])

            try:
                return response['access_token']
            except KeyError:
                raise Exception(response['error_description'])

        except Exception as ex:
            raise Exception('Error retrieving Access token\n' + str(ex))