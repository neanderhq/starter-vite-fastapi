"""Keep maintained recipe examples usable without model-generated metadata.

These focused checks catch example drift; the publisher's static validator is
authoritative. Run from any directory with PyYAML 6.0.3 installed.
"""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class DeploymentExamplesTests(unittest.TestCase):
    def test_base_stays_database_free(self):
        metadata = yaml.safe_load((ROOT / '.neander/compose.yaml').read_text())['x-neander']
        self.assertEqual(metadata['environment'], [])
        self.assertNotIn('migration', metadata)

    def test_database_and_auth_recipes_declare_complete_requirements(self):
        examples = list((ROOT / '.neander/blocks').glob('*/.neander/compose.yaml.example'))
        self.assertEqual(len(examples), 2)
        for path in examples:
            with self.subTest(block=path.parent.parent.name):
                recipe = yaml.safe_load(path.read_text())
                metadata = recipe['x-neander']
                self.assertIn(metadata['migration'], ('nextjs-drizzle', 'fastapi-alembic'))
                requirements = metadata['environment']
                names = [item['name'] for item in requirements]
                self.assertEqual(len(names), len(set(names)))
                self.assertIn('DATABASE_URL', names)
                for item in requirements:
                    self.assertTrue({'service', 'name', 'required', 'source', 'provider'} <= item.keys())
                    self.assertEqual(item['service'], 'web')
                    self.assertIs(item['required'], True)
                    if item['source'] == 'provisioned':
                        if item['name'] == 'DATABASE_URL':
                            self.assertEqual(item['provider'], 'Neon')
                        else:
                            self.assertEqual(item['provider'], 'Neander')
                            self.assertEqual(item['binding'], 'public_origin')
                    else:
                        self.assertIsNone(item['provider'])
                        self.assertIn(item['source'], ('user', 'generated'))
                        if item['source'] == 'generated':
                            self.assertEqual(item['generator'], 'opaque-random')
                if len(requirements) > 1:
                    self.assertEqual(len(requirements), 5)
                    self.assertEqual(metadata['ingress']['root_probe'], '/api/health')
                    self.assertIn('GOOGLE_CLIENT_ID', names)
                    self.assertIn('GOOGLE_CLIENT_SECRET', names)
                self.assertEqual(recipe['secrets'], {'neander_environment': {'file': '/run/neander/secrets/neander_environment'}})
                self.assertEqual(recipe['services']['web']['secrets'], ['neander_environment'])
                self.assertNotIn('environment', recipe['services']['web'])
                self.assertTrue((ROOT / recipe['services']['web']['build']['dockerfile']).is_file())


if __name__ == '__main__':
    unittest.main()
