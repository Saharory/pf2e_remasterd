# Publication and licensing review

Status: **local development baseline — not cleared for public release**

This document records a conservative publication boundary. It is not legal
advice. Policies and licenses can change, so their current text must be checked
again immediately before release.

## Recommended package split

1. **Community base system** — schemas, forms, views, styling, scripts, and
   generic Remaster mechanics. No compendium database.
2. **Open-rules modules** — only material confirmed as Licensed Material under
   the ORC License (or, separately, Open Game Content under the OGL), with all
   required notices and source attribution.
3. **Personal source modules** — content generated from purchased books,
   including extracted prose or art. These remain private and must not be
   committed or distributed.
4. **Experimental/personal features** — Remote Play and campaign-specific
   additions can live on a separate branch or in an optional add-on after the
   public base is stable.

## Current legal constraints

### Encounter+ upstream code

This work is derived from `https://github.com/encounterplus/pf2e` at commit
`832d839211c5d0354c8af2e85d7d9f938c1ff0dc`. No explicit license file was
present in that repository when this review was performed. Public visibility
does not by itself grant a general redistribution or relicensing right.

Before publishing binaries or a stand-alone copy, obtain clarification from
the Encounter+ maintainer about the license for the system code and assets.
Preserving the upstream Git history and attribution is required regardless.

### Paizo Community Use Policy

Paizo's Community Use Policy can cover freely available, non-commercial tools
and digital material that use Paizo intellectual property. A compliant project
must remain free and accessible without a paywall or unrelated access hurdles,
must carry Paizo's current required notice, must reproduce applicable author or
artist credits, and must provide visible up-to-date project contact
information. The policy also prohibits copying Paizo's trade dress.

The exact notice required by the policy as of the review date is:

> Pathfinder Second Edition Remaster system for Encounter+ uses trademarks
> and/or copyrights owned by Paizo Inc., used under Paizo's Community Use
> Policy (paizo.com/licenses/communityuse). We are expressly prohibited from
> charging you to use or access this content. Pathfinder Second Edition
> Remaster system for Encounter+ is not published, endorsed, or specifically
> approved by Paizo. For more information about Paizo Inc. and Paizo products,
> visit paizo.com.

**Before publication:** add a real, monitored contact method beside this
notice. Do not claim Paizo or Encounter+ endorsement.

### ORC Remaster rules

The ORC License covers functional game expressions such as rules, statblocks,
traits, classes, spells, actions, equipment mechanics, and character-sheet
methods when they are Licensed Material. It excludes Reserved Material such as
trademarks, trade dress, visual art, settings, locations, plots, characters,
organizations, and other protected proper-name material unless separately
licensed.

Any public module containing ORC Licensed Material needs the ORC Required
Notice, good-faith attribution to upstream licensors/creators, a Reserved
Material statement, and a statement identifying any expressly designated
Licensed Material. Do not relicense OGL-only material as ORC content.

### OGL legacy material

OGL content and ORC content require separate compliance paths. This project is
Remaster-focused; legacy OGL material should remain excluded unless a future
module deliberately includes the complete OGL notice and COPYRIGHT NOTICE and
clearly identifies its Open Game Content. OGL-only content cannot be converted
to ORC Licensed Material.

### Archives of Nethys and Foundry-derived data

Archives of Nethys publishes Paizo material under its own Community Use/OGL
notices and extensive source credits. Its public availability does not mean
that the site's compiled database, presentation, or API can automatically be
republished under an arbitrary software license. A public builder should fetch
only material independently permitted by the applicable Paizo/ORC/OGL terms,
retain source attribution, and avoid redistributing an AoN cache.

The PF2E for Foundry VTT project licenses its HTML/CSS/JavaScript under Apache
2.0, but its Pathfinder compendium content and art rely on separate Paizo and
Foundry licensing arrangements. Do not treat the entire Foundry repository as
Apache-licensed content. Any reused Apache code must retain the Apache license,
copyright notices, and modification notices.

## Asset hold

The current base inherits fonts, textures, a banner, and icons from the
Encounter+ upstream repository. No asset-license inventory accompanied that
repository. In particular, font files named FF Good, Gin, Sabon, and Taroca
must not be assumed redistributable. Book-like backgrounds and borders also
need review against the Community Use Policy's trade-dress restriction.

Before a public release, either:

- obtain and document redistribution permission for each asset; or
- replace it with an original or clearly open-licensed equivalent and record
  its license and source in an asset manifest.

## Publication checklist

- [ ] Encounter+ upstream code license confirmed in writing or in-repository
- [ ] every bundled font and image has a documented redistribution license
- [ ] Paizo trade-dress review completed
- [ ] current Community Use notice included and visible
- [ ] monitored project contact method included
- [ ] ORC/OGL notices generated per module and never mixed incorrectly
- [ ] author, artist, and upstream-project attribution included
- [ ] no PDFs, watermarks, extracted book prose, AoN cache, or campaign data
- [ ] no claim of endorsement by Paizo, Encounter+, Foundry, or Archives of Nethys
- [ ] clean-room archive inspection passes before uploading a release
