from decimal import Decimal

from app.models import SalesInvoice


class ValidationService:
    """Implements validation rules from BRD. Returns list of error dicts."""

    @staticmethod
    def validate_sales_invoice(invoice: SalesInvoice) -> list:
        """V-INV-01 to V-INV-05: Validate Sales Invoice fields"""
        errors = []

        if not invoice.invoice_number:
            errors.append({'field': 'invoice_number', 'message': 'Invoice number required'})

        if not invoice.exporter_name:
            errors.append({'field': 'exporter_name', 'message': 'Exporter name required'})

        if not invoice.buyer_name:
            errors.append({'field': 'buyer_name', 'message': 'Buyer name required'})

        if invoice.total_value is not None and invoice.total_value <= 0:
            errors.append({'field': 'total_value', 'message': 'Total value must be > 0'})

        if not invoice.currency:
            errors.append({'field': 'currency', 'message': 'Currency required'})

        return errors

    @staticmethod
    def validate_packing_list(doc_data: dict, invoice: SalesInvoice) -> list:
        """V-PL-01 to V-PL-03: Validate Packing List against invoice"""
        errors = []

        if doc_data.get('invoice_number') != invoice.invoice_number:
            errors.append({'field': 'invoice_number', 'message': 'Invoice number mismatch'})

        if doc_data.get('total_quantity', 0) <= 0:
            errors.append({'field': 'total_quantity', 'message': 'Total quantity must be > 0'})

        if doc_data.get('total_weight', 0) <= 0:
            errors.append({'field': 'total_weight', 'message': 'Total weight must be > 0'})

        return errors

    @staticmethod
    def validate_bol(doc_data: dict, invoice: SalesInvoice) -> list:
        """V-BOL-01 to V-BOL-04: Validate Bill of Lading against invoice"""
        errors = []

        if doc_data.get('shipper') != invoice.exporter_name:
            errors.append({'field': 'shipper', 'message': 'Shipper does not match invoice exporter'})

        if doc_data.get('consignee') != invoice.buyer_name:
            errors.append({'field': 'consignee', 'message': 'Consignee does not match invoice buyer'})

        if not doc_data.get('container_numbers'):
            errors.append({'field': 'container_numbers', 'message': 'At least 1 container required'})

        bol_value = Decimal(str(doc_data.get('total_value', 0)))
        if bol_value < invoice.total_value:
            errors.append({'field': 'total_value', 'message': 'BOL value less than invoice value'})

        return errors

    @staticmethod
    def validate_document(doc_type: str, doc_data: dict, invoice: SalesInvoice = None) -> list:
        """Dispatch to the correct validator by document type"""
        if doc_type == 'packing_list':
            return ValidationService.validate_packing_list(doc_data, invoice)
        if doc_type == 'bill_of_lading':
            return ValidationService.validate_bol(doc_data, invoice)
        if doc_type == 'sales_invoice':
            return ValidationService.validate_sales_invoice(invoice)
        return []
