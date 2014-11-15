


# This file defines the base class (interfaces) for signature extractors
# owner: rqi

#######################################################
# Abstract interfaces for signature extraction systems.

class SignatureExtractor:

    # Collect statistics and train parameters from training data.
    # trainingData is a dict with key:value including both samples and labels.
    # TODO: specify trainingData format
    def train(trainingData): raise NotImplementedError("Override me")

    # Extract a signature from a sample data x, return the signature.
    # TODO: specify x and return value format
    def extract(x): raise NotImplementedError("Override me")

