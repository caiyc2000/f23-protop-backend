import unittest
from unittest.mock import patch, Mock
from backend import aggregate_responses, call_apis
import json

MOCKED_ALPHAKNOT_RESPONSE = json.load(open('./tests/knotprot_response.json'))
MOCKED_PDB_RESPONSE = json.load(open('./tests/pdb_response.json'))
MOCKED_UNIPROT_RESPONSE = json.load(open('./tests/uniprot_response.json'))
MOCKED_KNOTPROT_RESPONSE = json.load(open('./tests/knotprot_response.json'))

class TestAggregation(unittest.TestCase):

    @patch('backend.call_alphaknot_api')
    @patch('backend.call_pdb_api')
    @patch('backend.call_uniprot_api')
    @patch('backend.call_knotprot_api')
    def test_aggregate_responses(self, mock_knotprot, mock_uniprot, mock_pdb, mock_alphaknot):
        """
        Test the aggregate_responses function with mocked API responses. These are Unittests.
        """
        
        mock_alphaknot.return_value = MOCKED_ALPHAKNOT_RESPONSE
        mock_pdb.return_value = MOCKED_PDB_RESPONSE
        mock_uniprot.return_value = MOCKED_UNIPROT_RESPONSE
        mock_knotprot.return_value = MOCKED_KNOTPROT_RESPONSE

        aggregated = aggregate_responses()

        # Sample assertions based on your aggregation logic
        self.assertIn("uniprot", aggregated)
        self.assertIn("uniprotID", aggregated["uniprot"])
        self.assertEqual(aggregated["data"]["knotprot"], "sample_knotprot_data")
        self.assertEqual(aggregated["data"]["pdb"], "sample_pdb_data")
        self.assertEqual(aggregated["data"]["uniprot"], "sample_uniprot_data")

class TestIntegration(unittest.TestCase):

    def test_call_apis(self):
        """
        Test real API calls
        """
        
        responses = call_apis()

        # Sample assertions based on expected responses
        self.assertIn("data", responses)
        self.assertIsInstance(responses["data"]["knotprot"], dict)
        self.assertIsInstance(responses["data"]["pdb"], dict)
        self.assertIsInstance(responses["data"]["uniprot"], dict)
        # Asserting that the pdb id matches expected pdb id
        self.assertEqual(responses["data"]["pdb"]["pdb_id"], "EXPECTED_PDB_ID")

if __name__ == '__main__':
    unittest.main()
