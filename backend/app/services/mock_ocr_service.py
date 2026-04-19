from uuid import uuid4


class MockOCRService:
    """
    Phase 1: Returns mocked OCR extraction data.
    Phase 2: Will call real SPR OCR API.
    """

    async def extract_sales_invoice(self, file_path: str) -> dict:
        """Mock extraction for Sales Invoice."""
        return {
            'invoice_number': f'EXP/{int(uuid4().int) % 10000}',
            'exporter_name': 'INZETMAN Private Limited',
            'buyer_name': 'UNIMACTS GLOBAL LLC',
            'invoice_date': '2025-04-18',
            'total_value': 150000.00,
            'currency': 'USD',
            'items': [
                {
                    'item_code': 'STL-BEAM-001',
                    'description': 'Structural Steel Beam I-Section',
                    'hsn_code': '7308.90.10',
                    'quantity': 100,
                    'unit': 'MT',
                    'unit_price': 1500.00,
                    'total_value': 150000.00,
                    'country_of_origin': 'India',
                    'is_metal': True,
                }
            ],
        }

    async def extract_packing_list(self, file_path: str) -> dict:
        """Mock extraction for Packing List."""
        return {
            'invoice_number': 'EXP/12345',
            'total_bundles': 50,
            'total_quantity': 100,
            'total_weight': 100.0,
            'items': [],
        }

    async def extract_bol(self, file_path: str) -> dict:
        """Mock extraction for Bill of Lading."""
        return {
            'bol_number': f'MSC{int(uuid4().int) % 1000000}',
            'shipper': 'INZETMAN Private Limited',
            'consignee': 'UNIMACTS GLOBAL LLC',
            'vessel_name': 'MSC GULSUN',
            'port_of_loading': 'INMAA2',
            'port_of_discharge': 'USNYC',
            'container_numbers': ['CONT123456'],
            'gross_weight': 100.0,
            'net_weight': 95.0,
            'total_packages': 50,
        }

    async def extract_boe(self, file_path: str) -> dict:
        """Mock extraction for Bill of Entry."""
        return {
            'boe_number': f'BOE{int(uuid4().int) % 1000000}',
            'total_duty': 5000.00,
            'hts_codes': ['7308.90.10'],
        }


mock_ocr_service = MockOCRService()
