__author__ = "Max Dippel, Michael Burkart and Matthias Urban"
__version__ = "0.0.1"
__license__ = "BSD"

import unittest
import numpy as np
import time

import torch
import ConfigSpace as CS
import ConfigSpace.hyperparameters as CSH
from autoPyTorch.utils.configspace_wrapper import ConfigWrapper
from autoPyTorch.pipeline.nodes.normalization_strategy_selector import NormalizationStrategySelector
from numpy.testing import assert_array_almost_equal
from sklearn.preprocessing import MinMaxScaler


class TestNormalizationStrategySelector(unittest.TestCase):


    def test_normalization_strategy_selector(self):
        X_train = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        X_valid = np.array([[3, 2, 1], [6, 5, 4], [9, 8, 7]])
        categorical_features = [False, True, False]
        hyperparameter_config = {NormalizationStrategySelector.get_name() +  ConfigWrapper.delimiter + "normalization_strategy": "minmax"}

        normalizer_node = NormalizationStrategySelector()
        normalizer_node.add_normalization_strategy("minmax", MinMaxScaler)

        fit_result = normalizer_node.fit(hyperparameter_config=hyperparameter_config, X_train=X_train, X_valid=X_valid,
            categorical_features=categorical_features)

        assert_array_almost_equal(fit_result['X_train'], np.array([[0, 0, 2], [0.5, 0.5, 5], [1, 1, 8]]))
        assert_array_almost_equal(fit_result['X_valid'], np.array([[2/6, -2/6, 2], [5/6, 1/6, 5], [8/6, 4/6, 8]]))
        assert_array_almost_equal(fit_result['categorical_features'], [False, False, True])

        X_test = np.array([[1, 2, 3]])

        predict_result = normalizer_node.predict(X=X_test, normalizer=fit_result["normalizer"])
        assert_array_almost_equal(predict_result['X'], np.array([[0, 0, 2]]))