import torch
import unittest
import torchtestcase


class DistributionTest(torchtestcase.TorchTestCase):
    """Base test for all distributions."""

    def assert_tensor_is_good(self, tensor, shape=None):
        self.assertIsInstance(tensor, torch.Tensor)
        self.assertFalse(torch.isnan(tensor).any())
        self.assertFalse(torch.isinf(tensor).any())
        if shape is not None:
            self.assertEqual(tensor.shape, torch.Size(shape))

    def assert_distribution_is_well_behaved(self, distribution, x, expected_shape=None):
        num_samples = x.shape[0]
        log_prob = distribution.log_prob(x)
        samples = distribution.sample(num_samples)
        samples2, log_prob2 = distribution.sample_with_log_prob(num_samples)
        log_prob2_match = distribution.log_prob(samples2)

        self.assert_tensor_is_good(log_prob, shape=(x.shape[0],))
        self.assert_tensor_is_good(samples, shape=x.shape)
        self.assert_tensor_is_good(log_prob2, shape=(x.shape[0],))
        self.assert_tensor_is_good(samples2, shape=x.shape)
        self.assertEqual(log_prob2, log_prob2_match)
        if expected_shape:
            self.assertEqual(samples.shape, expected_shape)
            self.assertEqual(samples2.shape, expected_shape)
