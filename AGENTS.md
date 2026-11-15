# spec-clauses-eu-law

This repository is spec-first. Keep clause JSON, module implementation, corpus, CI and publication gate in their separately scoped tickets.

Validate the specification with:

```bash
quire validate --scope . --module "$QUIRE_SPEC_ARTIFACTS_ISO_MODULE" "spec/**/*.md"
```

Public EU legislation and Commission guidance may be named and cited. Clause summaries must use original wording. Never name, number, quote or paraphrase a harmonised or other paywalled standard.
