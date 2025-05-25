import unittest
import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa os testes
from tests.test_routes import TestRoutes

if __name__ == '__main__':
    # Configura o test loader
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Adiciona os testes à suite
    suite.addTests(loader.loadTestsFromTestCase(TestRoutes))

    # Executa os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Sai com código de erro se algum teste falhou
    sys.exit(not result.wasSuccessful()) 