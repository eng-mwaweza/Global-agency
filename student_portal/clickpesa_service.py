"""
ClickPesa Payment Gateway Integration Service

This module handles all interactions with the ClickPesa API for payment processing.
Documentation: https://developer.clickpesa.com/
"""

import requests
import logging
import base64
import socket
import hashlib
import hmac
import json
from typing import Dict, Optional, Tuple
from django.conf import settings

logger = logging.getLogger(__name__)


class ClickPesaService:
    """Service class for ClickPesa payment gateway integration"""
    
    def __init__(self):
        # Import settings here to ensure latest values
        from django.conf import settings
        
        self.base_url = settings.CLICKPESA_BASE_URL
        self.client_id = settings.CLICKPESA_CLIENT_ID
        self.api_key = settings.CLICKPESA_API_KEY
        self.checksum = getattr(settings, 'CLICKPESA_CHECKSUM', '')
        
        # Debug logging
        logger.info(f"ClickPesa initialized with base_url: {self.base_url}")
        logger.info(f"Client ID length: {len(self.client_id) if self.client_id else 0}")
        logger.info(f"API Key length: {len(self.api_key) if self.api_key else 0}")
        logger.info(f"Checksum configured: {'Yes' if self.checksum else 'No'}")
        
        self._validate_credentials()
    
    def _validate_credentials(self):
        """Validate that credentials are properly configured"""
        if not self.client_id or self.client_id in ['your_client_id_here', 'your_actual_client_id_from_dashboard']:
            raise ValueError(
                "ClickPesa CLIENT_ID not configured. "
                "Please update CLICKPESA_CLIENT_ID in your .env file with valid credentials from https://dashboard.clickpesa.com"
            )
        if not self.api_key or self.api_key in ['your_api_key_here', 'your_actual_api_key_from_dashboard']:
            raise ValueError(
                "ClickPesa API_KEY not configured. "
                "Please update CLICKPESA_API_KEY in your .env file with valid credentials from https://dashboard.clickpesa.com"
            )
        if len(self.client_id) < 20 or len(self.api_key) < 20:
            logger.warning("ClickPesa credentials appear to be too short. Please verify they are correct.")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authorization headers - try X-API-Key header"""
        headers = {
            'X-API-Key': self.api_key,
            'X-Client-Id': self.client_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Django-Global-Agency/1.0'
        }
        logger.info(f"Authentication headers prepared - Client ID: {self.client_id[:8]}...{self.client_id[-4:]}, API Key: {self.api_key[:8]}...{self.api_key[-4:]}")
        return headers
    
    def _log_network_diagnostics(self):
        """Log network and domain diagnostics for troubleshooting"""
        try:
            # Get current domain/IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Check external IP
            try:
                external_ip_response = requests.get('https://httpbin.org/ip', timeout=5)
                external_ip = external_ip_response.json().get('origin', 'Unknown')
            except:
                external_ip = 'Could not determine'
            
            logger.info(f"NETWORK DIAGNOSTICS:")
            logger.info(f"  - Local hostname: {hostname}")
            logger.info(f"  - Local IP: {local_ip}")
            logger.info(f"  - External IP: {external_ip}")
            logger.info(f"  - Target API: {self.base_url}")
            
            # DNS resolution check
            try:
                api_host = self.base_url.replace('https://', '').replace('http://', '').split('/')[0]
                resolved_ip = socket.gethostbyname(api_host)
                logger.info(f"  - ClickPesa API resolved to: {resolved_ip}")
            except Exception as e:
                logger.error(f"  - DNS resolution failed: {e}")
                
        except Exception as e:
            logger.error(f"Network diagnostics failed: {e}")
    
    def _format_phone_number(self, phone_number: str) -> str:
        """Format phone number for ClickPesa API (ensure 255 prefix for Tanzania)"""
        # Remove any spaces, dashes, or plus signs
        phone = phone_number.replace(' ', '').replace('-', '').replace('+', '')
        
        # If starts with 0, replace with 255
        if phone.startswith('0'):
            phone = '255' + phone[1:]
        # If starts with 6,7,8 (common Tanzanian mobile prefixes), add 255
        elif phone.startswith(('6', '7', '8')) and len(phone) == 9:
            phone = '255' + phone
        # If doesn't start with 255, add it
        elif not phone.startswith('255'):
            phone = '255' + phone
            
        logger.info(f"Phone number formatted: {phone_number} -> {phone}")
        return phone
    
    def generate_order_reference(self, application_id: int) -> str:
        """Generate alphanumeric order reference like Node.js script"""
        import time
        import random
        
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        
        # Create alphanumeric reference (no special characters like Node.js)
        order_ref = f"APP{application_id}{timestamp}{random_num}"
        
        # Remove any non-alphanumeric characters (like Node.js script)
        clean_ref = ''.join(c for c in order_ref if c.isalnum())
        
        logger.info(f"Generated order reference: {clean_ref}")
        return clean_ref
    
    def _generate_dynamic_checksum(self, payload: dict) -> str:
        """Generate dynamic checksum like the working Node.js script"""
        try:
            # Remove checksum if it exists (like Node.js script)
            clean_payload = {k: v for k, v in payload.items() if k != 'checksum'}
            
            # Sort keys alphabetically (like Node.js script)
            sorted_keys = sorted(clean_payload.keys())
            
            # Convert all values to strings and concatenate
            payload_string = ''
            for key in sorted_keys:
                value = clean_payload[key]
                
                # Convert based on type (like Node.js script)
                if value is None:
                    value = ''
                elif isinstance(value, bool):
                    value = 'true' if value else 'false'
                elif isinstance(value, dict) or isinstance(value, list):
                    value = json.dumps(value)
                else:
                    value = str(value)
                
                payload_string += value
            
            logger.info(f"Checksum calculation:")
            logger.info(f"  - Sorted keys: {sorted_keys}")
            logger.info(f"  - Payload string: {payload_string}")
            logger.info(f"  - String length: {len(payload_string)}")
            
            # Generate HMAC SHA256 (like Node.js script)
            checksum = hmac.new(
                self.checksum.encode('utf-8'),
                payload_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            logger.info(f"Generated dynamic checksum: {checksum}")
            return checksum
            
        except Exception as e:
            logger.error(f"Dynamic checksum generation failed: {e}")
            return self.checksum if self.checksum else ""
    
    def _get_access_token(self) -> str:
        """Generate access token like the Node.js script"""
        try:
            url = f"{self.base_url}/generate-token"
            
            headers = {
                'client-id': self.client_id,
                'api-key': self.api_key,
                'Content-Type': 'application/json',
                'User-Agent': 'Django-Global-Agency/1.0'
            }
            
            logger.info(f"Generating access token from {url}")
            logger.info(f"Using headers: {list(headers.keys())}")
            
            response = requests.post(url, headers=headers, timeout=30)
            
            logger.info(f"Token response status: {response.status_code}")
            logger.info(f"Token response: {response.text[:200]}")
            
            if response.status_code == 200:
                data = response.json()
                if 'token' in data:
                    token = data['token']
                    logger.info(f"✅ Token generated successfully: {token[:50]}...")
                    return token
                else:
                    raise Exception(f"No token in response: {data}")
            else:
                # If ClickPesa indicates an IP/whitelist issue, collect network diagnostics
                resp_text = response.text or ''
                logger.error(f"Token generation failed: {response.status_code} - {resp_text}")
                if 'whitelist' in resp_text.lower() or 'ip address' in resp_text.lower() or 'ip' in resp_text.lower():
                    logger.error("Detected possible IP whitelist issue during token generation. Gathering network diagnostics...")
                    try:
                        self._log_network_diagnostics()
                    except Exception:
                        logger.exception("Failed while collecting network diagnostics for token generation error")
                raise Exception(f"Token generation failed: {response.status_code} - {resp_text}")
                
        except Exception as e:
            # Collect diagnostics for unexpected token generation errors as well
            logger.error(f"Token generation error: {e}")
            try:
                self._log_network_diagnostics()
            except Exception:
                logger.exception("Failed while collecting network diagnostics after token generation exception")
            raise e
    
    def _get_or_refresh_token(self) -> str:
        """ClickPesa uses direct API key authentication, no token needed"""
        return "direct_auth"
    

    
    def preview_ussd_push(
        self, 
        amount: float, 
        phone_number: str, 
        order_reference: str,
        currency: str = "TZS"
    ) -> Tuple[bool, Dict, str]:
        """
        Preview USSD-PUSH request to validate payment details
        
        Args:
            amount: Payment amount
            phone_number: Customer phone number (255XXXXXXXXX)
            order_reference: Unique order reference
            currency: Currency code (default: TZS)
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            # Step 1: Get access token (like Node.js script)
            access_token = self._get_access_token()
            
            url = f"{self.base_url}/payments/preview-ussd-push-request"
            
            # Format phone number properly
            formatted_phone = self._format_phone_number(phone_number)
            
            payload = {
                "amount": str(amount),
                "currency": currency,
                "orderReference": order_reference,
                "phoneNumber": formatted_phone,
                "fetchSenderDetails": True
            }
            
            # Add dynamic checksum (like Node.js script)
            if self.checksum:
                payload["checksum"] = self._generate_dynamic_checksum(payload)
                logger.info(f"Added dynamic checksum to payload")
            
            logger.info(f"Sending preview request to {url} with payload: {payload}")
            
            # Use token authentication (like Node.js script)
            headers = {
                'Authorization': access_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'Django-Global-Agency/1.0'
            }
            
            logger.info(f"Using token authentication: {access_token[:50]}...")
            
            response = requests.post(
                url, 
                json=payload, 
                headers=headers,
                timeout=30
            )
            
            logger.info(f"Preview response status: {response.status_code}")
            logger.info(f"Preview response headers: {dict(response.headers)}")
            logger.info(f"Preview response content: {response.text[:500]}")
            
            # Handle authentication errors with detailed diagnostics
            if response.status_code == 401:
                logger.error("=== 401 AUTHENTICATION ERROR DIAGNOSTICS ===")
                logger.error(f"Request URL: {url}")
                logger.error(f"Client ID used: {self.client_id}")
                logger.error(f"API Key used: {self.api_key[:10]}...{self.api_key[-6:]}")
                logger.error(f"Request headers sent: {headers}")
                logger.error(f"Response headers received: {dict(response.headers)}")
                logger.error(f"Full response content: {response.text}")
                
                # Check for common issues
                common_issues = []
                if 'domain' in response.text.lower() or 'whitelist' in response.text.lower():
                    common_issues.append("Domain not whitelisted in ClickPesa dashboard")
                if 'checksum' in response.text.lower() or 'signature' in response.text.lower():
                    common_issues.append("Missing or invalid checksum/signature")
                if 'expired' in response.text.lower():
                    common_issues.append("API credentials may be expired")
                if 'invalid' in response.text.lower():
                    common_issues.append("Invalid API credentials format")
                
                if common_issues:
                    logger.error(f"POSSIBLE CAUSES: {', '.join(common_issues)}")
                
                error_msg = (
                    f"Authentication failed (401 Unauthorized). "
                    f"Response: {response.text}. "
                    f"Possible issues: {', '.join(common_issues) if common_issues else 'Invalid credentials or domain not whitelisted'}. "
                    f"Please check: 1) Credentials in .env file, 2) Domain whitelist in ClickPesa dashboard, 3) Checksum requirements. "
                    f"Get valid credentials from https://dashboard.clickpesa.com"
                )
                logger.error(error_msg)
                return False, {}, error_msg
            
            # Try to parse JSON response
            try:
                data = response.json()
            except ValueError as json_error:
                if response.status_code == 200:
                    error_msg = f"Invalid JSON response from ClickPesa API. Status: {response.status_code}, Content: {response.text[:200]}"
                    logger.error(error_msg)
                    return False, {}, error_msg
                else:
                    error_msg = f"API error {response.status_code}: {response.text[:200]}"
                    logger.error(error_msg)
                    return False, {}, error_msg
            
            if response.status_code == 200:
                logger.info(f"USSD preview successful for order {order_reference}")
                return True, data, ""
            else:
                error_msg = data.get('message') or data.get('error') or f"Preview failed with status {response.status_code}"
                logger.error(f"USSD preview failed: {error_msg}")

                # If the API response indicates an IP whitelist issue, collect network diagnostics
                try:
                    check_text = (error_msg + ' ' + response.text).lower()
                except Exception:
                    check_text = str(error_msg).lower()

                if 'whitelist' in check_text or 'ip address' in check_text or 'ip' in check_text:
                    logger.error("Detected possible IP whitelist issue in preview response. Gathering network diagnostics...")
                    try:
                        self._log_network_diagnostics()
                    except Exception:
                        logger.exception("Failed while collecting network diagnostics for preview error")

                return False, data, error_msg
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error during preview: {str(e)}"
            logger.error(error_msg)
            try:
                logger.error("Network exception encountered during preview, gathering network diagnostics...")
                self._log_network_diagnostics()
            except Exception:
                logger.exception("Failed while collecting network diagnostics after network exception")
            return False, {}, error_msg
        except Exception as e:
            error_msg = f"Preview request error: {str(e)}"
            logger.error(error_msg)
            return False, {}, error_msg
    
    def initiate_ussd_push(
        self,
        amount: float,
        phone_number: str,
        order_reference: str,
        currency: str = "TZS"
    ) -> Tuple[bool, Dict, str]:
        """
        Initiate USSD-PUSH payment request
        
        Args:
            amount: Payment amount
            phone_number: Customer phone number (255XXXXXXXXX)
            order_reference: Unique order reference
            currency: Currency code (default: TZS)
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            # Step 1: Get access token (like Node.js script)
            access_token = self._get_access_token()
            
            url = f"{self.base_url}/payments/initiate-ussd-push-request"
            
            logger.info(f"Initiating USSD push for order {order_reference}")
            
            # Format phone number properly
            formatted_phone = self._format_phone_number(phone_number)
            
            payload = {
                "amount": str(amount),
                "currency": currency,
                "orderReference": order_reference,
                "phoneNumber": formatted_phone
            }
            
            # Add dynamic checksum (like Node.js script)
            if self.checksum:
                payload["checksum"] = self._generate_dynamic_checksum(payload)
                logger.info("Added dynamic checksum to initiate request")
            
            # Use token authentication (like Node.js script)
            headers = {
                'Authorization': access_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'Django-Global-Agency/1.0'
            }
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"USSD push initiated for order {order_reference}")
                return True, data, ""
            else:
                error_data = response.json()
                error_msg = error_data.get('message', 'Payment initiation failed')
                logger.error(f"USSD push failed: {error_msg}")
                return False, {}, error_msg
                
        except Exception as e:
            error_msg = f"Payment initiation error: {str(e)}"
            logger.error(error_msg)
            return False, {}, error_msg
    
    def check_payment_status(self, order_reference: str) -> Tuple[bool, Dict, str]:
        """
        Query payment status by order reference
        
        Args:
            order_reference: Unique order reference
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            url = f"{self.base_url}/payments/{order_reference}"
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Payment status retrieved for order {order_reference}")
                return True, data, ""
            else:
                error_msg = response.json().get('message', 'Status check failed')
                logger.error(f"Payment status check failed: {error_msg}")
                return False, {}, error_msg
                
        except Exception as e:
            error_msg = f"Status check error: {str(e)}"
            logger.error(error_msg)
            return False, {}, error_msg
    
    def preview_card_payment(
        self,
        amount: float,
        order_reference: str,
        currency: str = "USD"
    ) -> Tuple[bool, Dict, str]:
        """
        Preview card payment to validate details
        
        Args:
            amount: Payment amount
            order_reference: Unique order reference
            currency: Currency code (default: USD for card payments)
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            url = f"{self.base_url}/payments/preview-card-payment"
            
            payload = {
                "amount": str(amount),
                "currency": currency,
                "orderReference": order_reference
            }
            
            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Card payment preview successful for order {order_reference}")
                return True, data, ""
            else:
                error_msg = response.json().get('message', 'Preview failed')
                logger.error(f"Card preview failed: {error_msg}")
                return False, {}, error_msg
                
        except Exception as e:
            error_msg = f"Card preview error: {str(e)}"
            logger.error(error_msg)
            return False, {}, error_msg
    
    def initiate_card_payment(
        self,
        amount: float,
        order_reference: str,
        customer_email: str,
        customer_name: str,
        customer_phone: str = "",
        currency: str = "USD"
    ) -> Tuple[bool, Dict, str]:
        """
        Initiate card payment and get payment link
        
        Args:
            amount: Payment amount
            order_reference: Unique order reference
            customer_email: Customer email
            customer_name: Customer name
            customer_phone: Customer phone (optional)
            currency: Currency code (default: USD)
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            url = f"{self.base_url}/payments/initiate-card-payment"
            
            payload = {
                "amount": str(amount),
                "orderReference": order_reference,
                "currency": currency,
                "customer": {
                    "email": customer_email,
                    "name": customer_name,
                }
            }
            
            if customer_phone:
                payload["customer"]["phoneNumber"] = customer_phone
            
            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Card payment initiated for order {order_reference}")
                return True, data, ""
            else:
                error_msg = response.json().get('message', 'Card payment initiation failed')
                logger.error(f"Card payment failed: {error_msg}")
                return False, {}, error_msg
                
        except Exception as e:
            error_msg = f"Card payment error: {str(e)}"
            logger.error(error_msg)
            return False, {}, error_msg
    
    def get_account_balance(self) -> Tuple[bool, Dict, str]:
        """
        Get ClickPesa account balance
        
        Returns:
            Tuple of (success, response_data, error_message)
        """
        try:
            url = f"{self.base_url}/account/balance"
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info("Account balance retrieved successfully")
                return True, data, ""
            else:
                error_msg = response.json().get('message', 'Balance retrieval failed')
                logger.error(f"Balance check failed: {error_msg}")
                return False, {}, error_msg
                
        except Exception as e:
            error_msg = f"Balance check error: {str(e)}"
            logger.error(error_msg)
            return False, {}, error_msg


# Singleton instance
clickpesa_service = ClickPesaService()
