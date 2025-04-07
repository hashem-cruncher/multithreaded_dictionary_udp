#!/usr/bin/env python3
"""
JSON Dictionary Manager

This module handles loading and querying a dictionary stored in JSON format.
"""

import os
import json
import logging
import threading

# Configure logging
logger = logging.getLogger("Dictionary")


class DictionaryManager:
    """
    Dictionary manager that loads and queries a dictionary from a JSON file.
    Thread-safe implementation for concurrent access.
    """

    def __init__(self, dictionary_file):
        """
        Initialize the dictionary manager by loading entries from a JSON file.

        Args:
            dictionary_file (str): Path to the JSON dictionary file

        Raises:
            FileNotFoundError: If the dictionary file doesn't exist
            json.JSONDecodeError: If the JSON file is malformed
            Exception: For other errors
        """
        self.dictionary_file = dictionary_file
        self.dictionary_data = {}
        self.lock = threading.RLock()  # Reentrant lock for thread safety
        self.last_modified = 0

        # Load dictionary
        self._load_dictionary()

    def _load_dictionary(self):
        """
        Load the dictionary entries from the JSON file.

        Raises:
            FileNotFoundError: If the dictionary file doesn't exist
            json.JSONDecodeError: If the JSON file is malformed
            Exception: For other errors
        """
        if not os.path.exists(self.dictionary_file):
            raise FileNotFoundError(
                f"Dictionary file not found: {self.dictionary_file}"
            )

        # Check if file has been modified since last load
        file_modified = os.path.getmtime(self.dictionary_file)
        if file_modified <= self.last_modified:
            return  # File hasn't changed, no need to reload

        try:
            with open(self.dictionary_file, "r", encoding="utf-8") as file:
                dict_data = json.load(file)

                with self.lock:
                    # Validate dictionary format
                    if not isinstance(dict_data, dict) or "entries" not in dict_data:
                        raise ValueError(
                            "Invalid dictionary format. Expected 'entries' key."
                        )

                    # Process entries
                    self.dictionary_data = {}
                    entries = dict_data["entries"]

                    # Extract metadata if available
                    self.metadata = dict_data.get("metadata", {})

                    # Standardize dictionary format
                    for entry in entries:
                        word = entry.get("word", "").strip().lower()
                        definition = entry.get("definition", "")
                        synonyms = entry.get("synonyms", [])
                        category = entry.get("category", "")

                        if word and definition:
                            self.dictionary_data[word] = {
                                "definition": definition,
                                "synonyms": synonyms,
                                "category": category,
                            }

                    # Update last modified time
                    self.last_modified = file_modified

            logger.info(
                f"Loaded {len(self.dictionary_data)} entries from {self.dictionary_file}"
            )

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON dictionary file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading dictionary: {e}")
            raise

    def reload(self):
        """
        Reload the dictionary from the file.

        Returns:
            bool: True if dictionary was reloaded, False otherwise
        """
        try:
            self._load_dictionary()
            return True
        except Exception as e:
            logger.error(f"Error reloading dictionary: {e}")
            return False

    def lookup(self, word):
        """
        Look up a word in the dictionary.

        Args:
            word (str): The word to look up

        Returns:
            str or None: The definition of the word, or None if not found
        """
        word = word.strip().lower()

        with self.lock:
            entry = self.dictionary_data.get(word)
            if entry:
                return entry["definition"]
            return None

    def get_full_entry(self, word):
        """
        Get the full entry for a word including definition, synonyms, and category.

        Args:
            word (str): The word to look up

        Returns:
            dict or None: The full entry, or None if not found
        """
        word = word.strip().lower()

        with self.lock:
            return self.dictionary_data.get(word)

    def get_words_by_category(self, category):
        """
        Get all words in a specific category.

        Args:
            category (str): The category to filter by

        Returns:
            list: List of words in the category
        """
        with self.lock:
            return [
                word
                for word, entry in self.dictionary_data.items()
                if entry.get("category") == category
            ]

    def count(self):
        """
        Get the number of entries in the dictionary.

        Returns:
            int: The number of entries
        """
        with self.lock:
            return len(self.dictionary_data)

    def get_metadata(self):
        """
        Get dictionary metadata.

        Returns:
            dict: Dictionary metadata
        """
        with self.lock:
            return self.metadata.copy()
