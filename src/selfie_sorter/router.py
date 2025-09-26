"""
Handles classification of content based on explicit and suggestive rules.

The module facilitates classification of content into categories such
as 'safe', 'explicit', or 'suggestive'. It provides mechanisms for
evaluating both predefined rules and a coarse metric against configured
thresholds. The primary class, TagRouter, processes fine-grained data
to determine appropriate content labels.

Contains:
    - TagRouter:
      A class responsible for classification of content.
"""
from __future__ import annotations
from typing import Dict, List, Tuple, Optional

from .config import SortConfig


class TagRouter:
    """
    Handles classification of content based on explicit and suggestive rules.

    The TagRouter class is responsible for determining the classification of
    content into categories such as 'safe', 'explicit', or 'suggestive'. It
    uses predefined rules for explicit and suggestive content and can also
    evaluate a coarse metric against a configured threshold to make a decision.
    The class interacts with dictionaries containing potential labels for
    fine-grained classification and processes them accordingly.

    Attributes:
        cfg (SortConfig):
            Configuration object containing explicit and
            suggestive rules, as well as the NSFW threshold.

        explicit_rules (set):
            Processed set of explicit rules derived from
            the configuration.

        suggestive_rules (set):
              Processed set of suggestive rules derived
              from the configuration.
    """
    def __init__(self, cfg: SortConfig):
        """
        Initializes an instance of the `TagRouter` class with specific configuration and rules.

        Args:
            cfg (SortConfig):
                Configuration object containing explicit and suggestive rules.
        """
        self.cfg = cfg
        self.explicit_rules = {r.upper().replace(' ', '_') for r in cfg.explicit_rules}
        self.suggestive_rules = {r.upper().replace(' ', '_') for r in cfg.suggestive_rules}

    @staticmethod
    def _lbl(d: Dict) -> str:
        """
        Extracts and returns the label from a dictionary. The label is determined by checking the
        'd.label' key, and if not found, the 'd.class' key. If neither key exists, returns an empty string.

        Parameters:
            d (Dict):
                A dictionary potentially containing the keys 'label' or 'class'.

        Returns:
            str:
                The extracted label string with any surrounding whitespace removed.
        """
        return (d.get('label') or d.get('class') or '').strip()

    def classify(self, coarse: Optional[float], fine: List[Dict]) -> Tuple[str, List[str]]:
        """
        Classifies content based on coarse and fine classification inputs.

        This method applies classification rules to determine whether the content is
        safe, explicit, or suggestive using coarse and fine-grained information. It
        leverages thresholds and matching labels for decision-making.

        Parameters:
            coarse (Optional[float]):
                Coarse-grained classification score; could be None.

            fine (List[Dict]):
                Fine-grained classification data containing detailed
                labels for analysis.

        Returns:
            Tuple[str, List[str]]:
                A tuple containing a classification label ('safe', 'explicit', or 'suggestive')
                and a list of raw labels that contributed to the decision.
        """
        raw_labels = sorted({self._lbl(d) for d in fine if self._lbl(d)})
        labels_upper = [l.upper().replace(' ', '_') for l in raw_labels]

        if coarse is not None and coarse < self.cfg.nsfw_threshold and not labels_upper:
            return ('safe', [])

        if any(l in self.explicit_rules for l in labels_upper):
            return ('explicit', raw_labels)

        if any(l in self.suggestive_rules for l in labels_upper):
            return ('suggestive', raw_labels)

        if coarse is not None and coarse >= self.cfg.nsfw_threshold:
            return ('suggestive', raw_labels)

        return ('safe', raw_labels)


__all__ = [
    'TagRouter',
]
