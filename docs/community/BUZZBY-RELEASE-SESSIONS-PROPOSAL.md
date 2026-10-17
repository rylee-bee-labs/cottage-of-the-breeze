# 🐝 Buzzby release sessions: editorial proposal for Claude review

**Status:** DESIGN PROPOSAL, not an implementation or release approval.
**Initiator:** Rylee + Sol, 2026-10-17.
**Pilot:** Cottage of the Breeze, existing draft PR #192. Eventually reusable across public Rylee-Bee Labs projects.

## North star

Buzzby is an openly AI-powered, MMO-style community manager and the projects' *biggest fan*. She translates **real** work into tiny joyful updates. She is personable, sometimes complimentary, curious about players, generous about contributors, and never a corporate status bot. Default post: 40–100 words with a great screenshot when one exists. Readers should understand what's playable now, what's being made, and how to join in.

**New decision to incorporate:** Buzzby is a *recurring character*, not a static marketing asset. Don't front-load an art pack. Preserve a few recognizable identity anchors (friendly bee, navy workshop jacket, golden details, small messenger satchel, expressive eyes). Each editorial session creates **fresh writing and an original scene/illustration** informed by that edition's real news. A stable avatar is fine, but never pass off generated editorial illustration as an in-game screenshot. Keep image provenance and alt text.

## Two triggers, not one

1. **Release session**: candidate exists for a public deliverable (game build, tool, website release). Build evidence first; Buzzby's editorial/design packet is part of release review, *not proof that the release shipped*.
2. **Community update session**: worthwhile milestone, weekly postcard, screenshot or follow-up, **without making it a formal release**. Don't create a GitHub Release just to feed the posting cadence. Skip quiet weeks.

## Release-session pipeline

1. **Evidence intake.** Pin source repos/SHAs, build artifact location and digest where available, release candidate status, user-facing differences, compatible versions, licensing/provenance, test receipts, human acceptance status, approved story/canon, issue links. UNKNOWN stays unknown. Private infrastructure details stay private.
2. **Editorial session.** Buzzby picks one delightful hook and at most three meaningful updates; writes a short headline/post, fun human changelog, Buzzboard change *only if status changed*, and drafts replies/follow-up pointers if needed. Don't publish internal commit listings.
3. **Visual session.** Pick a **verified actual screenshot** with build/ref evidence if available. Create a distinct Buzzby illustration brief and generated art for this edition where tooling and permission permit. Distinguish **verified gameplay**, **concept/draft**, and **Buzzby editorial illustration** in captions. No fake screen/game feature.
4. **OpenDesign + normal review.** Use the estate's *actual* OpenDesign/review path (inspect and reuse; don't invent an API). Review accuracy, personality, visual quality, character consistency, non-recycled composition, clarity, accessibility, provenance, spoilers, claims, and links. Keep owner approval for new canon, publication, commitments or sensitive replies. Preserve regular code/build/release gates, not replace them with editorial signoff.
5. **Single review packet.** PR or existing Project Home review containing text, artwork, screenshot proofs, proposed tags/version/release notes, roadmap delta, source citations, and a preview. Rylee sees a small **Glance** version first, with detailed inspection available; reviewers should not need to replay the whole evidence chain. Changes can be revised without starting over.
6. **Publish after approvals.** Only approved assets/copy go to repo README, GitHub Release or Discussion, gallery, and optionally ryleebee.com. Verify the final destinations, record what was actually published, and follow up on community questions. No default auto-post or auto-merge in v1.

## Do we need *actual* releases?

**Please audit rather than assume.** Cottage has a historically named “Release 1” playable gallery build (2026-10-04), plus a separate **1.0 release epic** (#170) still gated on human play, physical phone, and release audit. VEFR's SECURITY.md refers to release tags. This does **not** prove that formal GitHub Releases/version tags are consistently used. Check each relevant public repo's actual tags, GitHub Releases, artifact stability, workflow and protections.

**Proposed semantics for review:**
- **Dev diary / workshop postcard:** update only, no tag or Release required.
- **Preview / alpha / beta build:** optional pre-release tag and GitHub prerelease if artifact is actually reproducible, playable and approved for sharing. Explicit “preview,” not 1.0.
- **Actual release:** immutable repo version/tag, linked verified artifact with dual-repo SHAs when relevant, release notes and known limitations, and the existing release/publication gates completed. Don't promote 1.0 from a passing CI check or merged roadmap.
- **Hotfix:** short factual notes; reuse assets or a simple Buzzby portrait if new illustration would slow down a safety fix. Never let illustration block urgent fixes.

Avoid converting every merged PR or nightly build into a “release.” Keep the release ledger with repo-native tags/releases and existing provenance, **not a parallel Buzzby truth store**.

## Pilot acceptance

For Cottage only: one fully assembled **draft** release/community packet with (a) 60–100 word post, (b) friendly changelog, (c) honest Buzzboard status, (d) newly generated Buzzby illustration/brief, (e) a **real verified** game screenshot, (f) provenance/alt text, (g) linked evidence, and (h) a review receipt. No automatic public publication. Use #192 as the starting editorial proposal, not as permission to add gameplay work or to bypass existing canon/release gates.

## Requested Claude feedback (before building)

1. What existing mission/skill, OpenDesign, PR and owner-review workflow should host this with the **fewest new parts**?
2. Do the public repos have real GitHub Releases/tags today? If inconsistent, propose **minimum** migration, by repo, preserving existing gallery builds and 1.0 gates. Is there any reason *not* to add formal releases now?
3. What trigger/event reliably detects “release candidate ready for editorial session” versus a routine community update?
4. Where should immutable image, alt text, prompts and build/screenshot provenance live so PR review stays clean?
5. What is the minimal failure/rollback path when art generation, approval, upload or publishing fails? How do we avoid duplicate release announcements?
6. What parts of this are unnecessary? Cut scope aggressively. Suggest one end-to-end pilot proof and return **feedback only**, with tradeoffs, before we authorize implementation.

Remember: Rylee wants Buzzby to be fun, light, a little silly, and a real recurring character. This is a community-facing creative role, not an extra platform team.
