class TestInputPhrase:
    def test_input_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, "Phrase longer than 15 characters"
