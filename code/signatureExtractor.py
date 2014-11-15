


# This file defines the base class (interfaces) for signature extractors
# owner: rqi

#######################################################
# Abstract interfaces for signature extraction systems.

class SignatureExtractor:

    # Collect statistics and train parameters from training data.
    # trainingData is a dict with key:value including both samples and labels.
    # TODO: specify trainingData format
    def train(self, trainingData): raise NotImplementedError("Override me")

    # Extract a signature from a sample data x, return the signature.
    # TODO: specify x and return value format
    def extract(self, x): raise NotImplementedError("Override me")

    # Compute distance of two signatures
    def distance(self, s1, s2): raise NotImplementedError("Override me")

