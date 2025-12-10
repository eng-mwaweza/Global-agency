"""
ClickPesa Payment Gateway Integration Service

This module handles all interactions with the ClickPesa API for payment processing.
Documentation: https://developer.clickpesa.com/
"""

import requests
import logging
import base64
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
        
        # Debug logging
        logger.info(f"ClickPesa initialized with base_url: {self.base_url}")
        logger.info(f"Client ID length: {len(self.client_id) if self.client_id else 0}")
        logger.info(f"API Key length: {len(self.api_key) if self.api_key else 0}")
        
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
            'Accept': 'application/json'
        }
        logger.debug(f"Request headers: X-Client-Id={self.client_id[:10]}..., X-API-Key={self.api_key[:10]}...")
        return headers
    
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
            url = f"{self.base_url}/payments/preview-ussd-push-request"
            
            payload = {
                "amount": str(amount),
                "currency": currency,
                "orderReference": order_reference,
                "phoneNumber": phone_number,
                "fetchSenderDetails": True
            }
            
            logger.info(f"Sending preview request to {url} with payload: {payload}")
            
            response = requests.post(
                url, 
                json=payload, 
                headers=self._get_headers(),
                timeout=30
            )
            
            logger.info(f"Preview response status: {response.status_code}")
            logger.info(f"Preview response content: {response.text[:500]}")
            
            # Handle authentication errors specifically
            if response.status_code == 401:
                error_msg = (
                    "Authentication failed (401 Unauthorized). Your ClickPesa credentials are invalid or expired. "
                    "Please verify your CLICKPESA_CLIENT_ID and CLICKPESA_API_KEY in the .env file. "
                    "Get valid credentials from https://dashboard.clickpesa.com"
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
                return False, data, error_msg
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error during preview: {str(e)}"
            logger.error(error_msg)
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
            url = f"{self.base_url}/payments/initiate-ussd-push-request"
            
            logger.info(f"Initiating USSD push for order {order_reference}")
            
            payload = {
                "amount": str(amount),
                "currency": currency,
                "orderReference": order_reference,
                "phoneNumber": phone_number
            }
            
            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
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
