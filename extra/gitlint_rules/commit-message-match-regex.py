from gitlint.rules import CommitRule, RegexOption, RuleViolation


class CommitMessageRegexMatches(CommitRule):  # type: ignore[misc]
    name = "commit-message-match-regex"
    id = "UC1"
    options_spec = [RegexOption("regex", None, "Regex the commit message should match")]

    # pylint: disable=inconsistent-return-statements
    def validate(self, commit):  # type: ignore[no-untyped-def]
        if not self.options["regex"].value:
            return

        if not self.options["regex"].value.search(commit.message.original):
            violation_msg = (
                "Commit message does not match regex "
                f"({self.options['regex'].value.pattern})"
            )

            return [
                RuleViolation(
                    self.id, violation_msg, None, len(commit.message.original) + 1
                )
            ]
