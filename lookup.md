AI GENERATED, CLAUDE SONNET5.5 @ MEDIUM EFFORT


# .lookup - codebase map
# Generated 2026-10-14 by gen_lookup.py. Auto sections regenerate; Verdict/Notes/PLAN are for hand edits.

## 1. Identity
- Mod: Changed: Synergy (mod_id `changed_synergy`, group `net.parkabird.changedsynergy`)
- Upstream author: ParkaBird   License: GNU General Public License v3.0 or later
- Version at fork point: 1.1.3+mc1.20.1-changed0.15.7
- Target: Minecraft 1.20.1, Forge 47.4.21, mappings official
- Source size: 350 Java files, 72691 lines; 88 mixin classes
- Fork goal: LTS rewrite - deeper behaviors, new features, wider compat
- Fork repo: goldfinder/changed-charged-synergy

## 2. Dependency direction (from docs/ARCHITECTURE.md)
- Hard dep: Changed. Optional: Addon Plus, Additions, Extras, Vanilla, Domestication Innovation, Curios, FurMutage, Survive Protocol, firearms mods.
- Optional-mod types must stay under `compat/` (`compat/addon` for signatures using Addon types). They must NOT leak into the main class, api, menus, packets, or client state.
- Layers: init/registries -> ai (state + services + goals) -> event (Forge hooks) -> dialogue -> world.inventory (menus) -> network -> client.

## 3. Package map
| Package | Files | Lines | Purpose | First-pass verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| ai | 101 | 35148 | Core gameplay: relationships, bonds, factions, settlements, grabs, hypnosis, takeover, hunting | ? |  |
| client | 58 | 11101 | Screens, radial menus, renderers, client state | ? |  |
| event | 17 | 6064 | Forge event handlers (social, hunt AI, reputation, territory, disguises) | ? |  |
| mixin | 88 | 4930 | Patches to Changed / Addon Plus / vanilla / other mods | ? |  |
| world/inventory | 11 | 4448 | Menus / containers (social, bonded inventory, relationship) | ? |  |
| compat/addon | 8 | 2629 | Classes whose signatures use Changed Addon Plus types (load only if present) | ? |  |
| dialogue | 4 | 2486 | Contextual NPC lines, emotes, translation selection | ? |  |
| network | 27 | 1317 | SimpleChannel packets and sync | ? |  |
| command | 4 | 1201 | Server commands (bond, config, spawn) | ? |  |
| compat | 6 | 1098 | Optional-mod bridges (Addon Plus, Extras, Vanilla, Domestication, firearms) | ? |  |
| (root) | 3 | 624 | Mod entry point + common/client config | ? |  |
| world | 4 | 542 | World-level helpers, biome/territory | ? |  |
| init | 7 | 271 | DeferredRegister registries + gamerules | ? |  |
| compat/curios | 2 | 234 | Curios integration | ? |  |
| performance | 1 | 231 | Performance snapshot/measurement | ? |  |
| entity | 1 | 91 | Entity classes | ? |  |
| recipe | 1 | 66 | Recipe serializers | ? |  |
| advancement | 1 | 61 | Advancement triggers | ? |  |
| api | 2 | 54 | Stable integration surface for other mods | ? |  |
| item | 2 | 46 | Items | ? |  |
| effect | 1 | 29 | Mob effects | ? |  |
| util | 1 | 20 | Misc helpers | ? |  |

## 4. Entry points and registration
- Main class: `ChangedSynergyMod` (`@Mod`). Registers COMMON + CLIENT configs, network channel, optional compat events, then DeferredRegisters.
- Registries (init/): Entities, Items, Menus, MobEffects, RecipeSerializers, SoundEvents, GameRules.
- Access transformer: `META-INF/accesstransformer.cfg` (GameRules create, Mob goalSelector/persistenceRequired, goal speed modifiers, Entity shared flag).
- Mixin config: `changed_synergy.mixins.json` (required=true, defaultRequire=1 -> any failed injection crashes load).

## 5. Persistence (breaking these breaks existing worlds)
- Creature NBT compound `ChangedSynergySocial`; player compounds prefixed `ChangedSynergy`.
- SavedData classes:
  - `src/main/java/net/parkabird/changedsynergy/ai/BondedCreatureDeathData.java` (95 lines)
  - `src/main/java/net/parkabird/changedsynergy/ai/BondedCreatureReleaseData.java` (87 lines)
  - `src/main/java/net/parkabird/changedsynergy/ai/BondedRevivalData.java` (118 lines)
  - `src/main/java/net/parkabird/changedsynergy/ai/CreatureCommunityData.java` (968 lines)
  - `src/main/java/net/parkabird/changedsynergy/ai/CreatureMorphAliasData.java` (98 lines)
  - `src/main/java/net/parkabird/changedsynergy/ai/CreatureRelationshipForgetData.java` (65 lines)
  - `src/main/java/net/parkabird/changedsynergy/ai/PlayerOutpostData.java` (299 lines)
  - `src/main/java/net/parkabird/changedsynergy/world/OrangeLeafRegrowthData.java` (173 lines)
- DECISION NEEDED: keep mod_id / NBT keys / gamerule names / channel name for save-compat with upstream, or break compat and migrate.

## 6. Network packets
- AbsorptionNegotiationStatePacket, BondedInventoryOpenPacket, ChangedSynergyNetwork, EmoteTransitionPacket, ExoskeletonMotionPacket, FriendlySocialHugState, FriendlySocialHugSyncPacket, FriendlySuitSyncPacket, GrabQteSyncPacket, HypnosisQteSyncPacket, MergedPlayerIdentityPacket, NativePetReassimilatePacket, OpenAbsorptionNegotiationPacket, PatAnimationControlPacket, PatAnimationPacket, PatAnimationSpeedPacket, PerformanceSnapshotPacket, PlayerRelationshipOpenPacket, ProvisionerTradeSyncPacket, RevivalGrabAbilityPacket, ScoutTargetPacket, TakeoverActionPacket, TakeoverStatePacket, TelepathyDialoguePacket, TerritorySyncPacket, TransfurVisualPacket, WhiteHiveTargetsPacket

## 7. Mixins
| Mixin | Side | Target | Lines | Verdict | Notes |
| --- | --- | --- | --- | --- | --- |
| AbilityRadialNegotiationMixin | client | value = AbilityRadialScreen, remap = false | 129 | ? |  |
| AbilityRadialScreenCloseMixin | client | value = AbilityRadialScreen, remap = false | 27 | ? |  |
| AddonCarryMountPoseMixin | client |  targets = "net.foxyas.changedaddon.client.model.animations.CarryAbilityAnimation", remap = false | 34 | ? |  |
| BetterCombatFriendlyWrapTargetMixin | client | targets = "net.bettercombat.client.collision.TargetFinder", remap = false | 38 | ? |  |
| ChangedEntityPatPoseMixin | client | AdvancedHumanoidModel | 30 | ? |  |
| EmoteParticleMixin | client | value = EmoteParticle, remap = false | 56 | ? |  |
| GrabOverlayAnimationMixin | client | value = GrabOverlay, remap = false | 80 | ? |  |
| HeldCreaturePositionMixin | client | value = LatexHeldEntityLayer, remap = false | 34 | ? |  |
| HumanPlayerPreviewMixin | client | value = EventHandlerClient, remap = false | 29 | ? |  |
| HypnosisClientCameraGuardMixin | client | value = CameraUtil, remap = false | 31 | ? |  |
| HypnosisClientControlMixin | client | Minecraft | 52 | ? |  |
| HypnosisClientEffectGuardMixin | client | LivingEntity | 37 | ? |  |
| HypnosisKeyboardControlMixin | client | KeyboardHandler | 33 | ? |  |
| HypnosisMouseControlMixin | client | MouseHandler | 51 | ? |  |
| HypnosisMovementInputMixin | client | KeyboardInput | 36 | ? |  |
| NativeRadialFrameAlphaMixin | client |  value = {VariantRadialScreen, TamedDarkLatexScreen}, remap = false | 43 | ? |  |
| PlayerPatPoseMixin | client | PlayerModel | 29 | ? |  |
| RadialScreenAnimationMixin | client | value = AbstractRadialScreen, remap = false | 779 | ? |  |
| RepairedDarkLatexMaskLayerMixin | client | DarkLatexMaskLayer | 41 | ? |  |
| SharedRestCameraMixin | client | value = Camera, priority = 900 | 31 | ? |  |
| TaczAdditionsSuitGunTuckMixin | client | targets = "com.raiiiden.taczadditions.util.GunTuckMath", remap = false | 31 | ? |  |
| TakeoverAbilityPacketMixin | client | value = SimpleChannel, remap = false | 26 | ? |  |
| TakeoverHypnosisIsolationMixin | client | value = HypnosisQteClientState, remap = false | 39 | ? |  |
| TakeoverKeyboardMixin | client | KeyboardHandler | 30 | ? |  |
| TakeoverLocalPlayerMixin | client | LocalPlayer | 17 | ? |  |
| TakeoverMinecraftMixin | client | Minecraft | 26 | ? |  |
| TakeoverMouseMixin | client | MouseHandler | 45 | ? |  |
| TakeoverMovementInputMixin | client | KeyboardInput | 21 | ? |  |
| TaurChestPackNpcMixin | client | value = TaurChestPackLayer, remap = false | 32 | ? |  |
| WhiteHiveTargetColorMixin | client | value = Entity, remap = false | 45 | ? |  |
| WhiteHiveTargetGlowMixin | client | value = Minecraft, remap = false | 45 | ? |  |
| AddonAlphaLeapGrabMixin | common | targets = "net.foxyas.changedaddon.entity.ai.goals.generic.attacks.LeapDiveGoal", remap = false | 31 | ? |  |
| AddonNativeSuitGoalGuardMixin | common | targets = "net.foxyas.changedaddon.entity.ai.LatexSuitOwnerGoal", remap = false | 30 | ? |  |
| AddonThunderDashCarryMixin | common | targets = "net.foxyas.changedaddon.entity.ai.goals.exp9.ThunderDashAttack", remap = false | 27 | ? |  |
| AddonThunderDiveCarryMixin | common | targets = "net.foxyas.changedaddon.entity.ai.goals.exp9.ThunderDiveGoal", remap = false | 29 | ? |  |
| AquaticGoToWaterRoutineMixin | common | targets = "net.ltxprogrammer.changed.entity.beast.AbstractAquaticEntity$GoToWaterGoal" | 41 | ? |  |
| BeehivePlacementMixin | common | value = SurfaceNBTPiece, remap = false | 51 | ? |  |
| BondedInfuserRecipeMixin | common | value = InfuserMenu, remap = false | 52 | ? |  |
| BondedRevivalVesselUseMixin | common | value = {LatexSyringe, LatexFlask}, remap = false | 26 | ? |  |
| CentaurControllingPassengerMixin | common | Mob | 36 | ? |  |
| CentaurHorseInterfaceMixin | common | value = ChangedEntity, remap = false | 51 | ? |  |
| CentaurRideControlMixin | common | LivingEntity | 131 | ? |  |
| ChangedEntityAbilityInvoker | common | value = ChangedEntity, remap = false | 15 | ? |  |
| ChangedEntityAiTimingMixin | common | Mob | 39 | ? |  |
| ChangedEntityInheritedEyesMixin | common | value = ChangedEntity, remap = false | 36 | ? |  |
| ChangedExtrasLatexBrainMixin | common |  targets = "com.katt.changedextras.common.ai.LatexBrain", remap = false | 52 | ? |  |
| ChangedExtrasSmartAiHandlerMixin | common |  targets = "com.katt.changedextras.common.ai.LatexMobAIHandler", remap = false | 51 | ? |  |
| ChangedKeepConsciousDefaultMixin | common | value = ChangedGameRules, remap = false | 41 | ? |  |
| DarkLatexWolfPupAgeAccessor | common | DarkLatexWolfPup | 16 | ? |  |
| DarkLatexWolfPupMorphMixin | common | DarkLatexWolfPup | 49 | ? |  |
| DomesticationInnovationTameableUtilsMixin | common | targets = "com.github.alexthe668.domesticationinnovation.server.entity.TameableUtils", remap = false | 80 | ? |  |
| ExoskeletonRestrainTakeoverMixin | common | value = Exoskeleton.ExoskeletonRestrainGoal, remap = false | 67 | ? |  |
| ExoskeletonTakeoverItemStateMixin | common | value = Exoskeleton, remap = false | 19 | ? |  |
| FiniteEntityPushMixin | common | Entity | 20 | ? |  |
| FriendlyLatexSleepMixin | common | ChangedEntity | 36 | ? |  |
| GrabAssimilationModeMixin | common | value = GrabEntityAbilityInstance, remap = false | 50 | ? |  |
| GrabQteSyncMixin | common | value = GrabEntityAbilityInstance, remap = false | 286 | ? |  |
| HurtByTargetGoalNullGuardMixin | common | HurtByTargetGoal | 36 | ? |  |
| HypnosisAbilityMixin | common | value = HypnosisAbility, remap = false | 20 | ? |  |
| HypnosisCameraGuardMixin | common | value = CameraUtil, remap = false | 29 | ? |  |
| HypnosisChangedEntityAttackGuardMixin | common | value = ChangedEntity, remap = false | 34 | ? |  |
| HypnosisEffectGuardMixin | common | LivingEntity | 53 | ? |  |
| HypnosisMobAttackGuardMixin | common | Mob | 34 | ? |  |
| LabTablePathfindingMixin | common | WalkNodeEvaluator | 32 | ? |  |
| MonsterDaylightSpawnMixin | common | Monster | 31 | ? |  |
| NonEntityMerchantSoundMixin | common | MerchantMenu | 26 | ? |  |
| OrganicEvacuationDropGuardMixin | common |  targets = "net.foxyas.changedaddon.entity.api.IGrabberEntity", remap = false | 61 | ? |  |
| OrganicTransfurRestrictionMixin | common | value = ChangedEntity, remap = false | 77 | ? |  |
| OverworldBiomeBuilderMixin | common | OverworldBiomeBuilder | 81 | ? |  |
| PinkShortsAccessoryTickMixin | common | value = PinkShorts, remap = false | 17 | ? |  |
| RandomizedTransfurDecisionMixin | common | value = TransfurEvents.LatexAssimilationDecisionEvent, remap = false | 24 | ? |  |
| RelationshipPeacefulDespawnMixin | common | Mob | 45 | ? |  |
| SocialMobCombatGuardMixin | common | LivingEntity | 51 | ? |  |
| SocialTargetGuardMixin | common | value = ChangedEntity, remap = false | 80 | ? |  |
| SpawnPlacementsDaylightContextMixin | common | SpawnPlacements | 40 | ? |  |
| SurfaceSystemMixin | common | SurfaceSystem | 45 | ? |  |
| TakeoverAbsorptionMixin | common | value = LatexAssimilationDecision, remap = false | 63 | ? |  |
| TakeoverExtraJumpPacketMixin | common | value = ExtraJumpKeybind, remap = false | 31 | ? |  |
| TakeoverGrabMixin | common | value = GrabEntityAbilityInstance, remap = false, priority = 1100 | 140 | ? |  |
| TakeoverNativeServerPacketMixin | common | value = {VariantAbilityActivate, GrabEntityPacket, GrabEntityPacket.EscapeKeyState}, remap = false | 53 | ? |  |
| TakeoverPlayerAbsorptionMixin | common | targets = "net.ltxprogrammer.changed.entity.ai.EntityAssimilationBehavior$PlayerAssimilationBehavior", remap = false | 49 | ? |  |
| TakeoverServerInputMixin | common | ServerGamePacketListenerImpl | 45 | ? |  |
| TakeoverUntransfurCommandMixin | common | targets = "net.ltxprogrammer.changed.command.CommandTransfur", remap = false | 28 | ? |  |
| TransfurVariantInstanceInheritedEyesMixin | common | value = TransfurVariantInstance, remap = false | 56 | ? |  |
| VanillaOakFoliageMixin | common | value = TreeFeatures, priority = 1500 | 46 | ? |  |
| VariantAbilityActivateMixin | common | value = VariantAbilityActivate, remap = false | 70 | ? |  |
| WhiteLatexPillarContactMixin | common | value = WhiteLatexTransportInterface.EventSubscriber, remap = false | 97 | ? |  |
| WhiteLatexTerritorySpawnMixin | common | value = SpreadingLatexType.WhiteLatex, remap = false | 97 | ? |  |
- Mixins listed in json but missing a source file, or source files not listed (UNLISTED), are bugs worth checking.

## 8. Hotspots (largest files, refactor candidates)
| File | Lines | Role |
| --- | --- | --- |
| ai/CreatureSettlementService.java | 4348 | service |
| ai/InvoluntaryTransfurNegotiation.java | 2612 | model/util |
| event/LatexSocialEvents.java | 2251 | events |
| ai/LatexSocialMemory.java | 1896 | state |
| ai/TakeoverService.java | 1714 | service |
| dialogue/NpcDialogue.java | 1714 | dialogue |
| compat/addon/ChangedAddonSocialEvents.java | 1278 | compat |
| world/inventory/SocialInteractionMenu.java | 1191 | menu |
| ai/CreaturePersonality.java | 1148 | model/util |
| event/HuntAIEvents.java | 1111 | events |
| ai/BondedSuitService.java | 1008 | service |
| ai/CreatureRoutineGoal.java | 989 | ai-goal |
| ai/CreatureCommunityData.java | 968 | saved-data |
| ai/HypnosisQteService.java | 810 | service |
| world/inventory/BondedCreatureInventoryMenu.java | 799 | menu |
| ai/ProvisionerTradeService.java | 785 | service |
| mixin/RadialScreenAnimationMixin.java | 779 | mixin |
| client/SocialInteractionScreen.java | 771 | client |
| client/ChangedSynergyConfigScreen.java | 765 | client |
| ai/CreatureIdentity.java | 752 | model/util |
| world/inventory/PlayerRelationshipMenu.java | 649 | menu |
| ai/ExoskeletonTakeoverAdapter.java | 647 | model/util |
| client/PlayerRelationshipScreen.java | 634 | client |
| ai/BondedRevivalService.java | 632 | service |
| command/BondCommand.java | 621 | command |

## 9. Resources
| Directory | Files |
| --- | --- |
| . | 3 |
| META-INF | 2 |
| assets | 0 |
| assets/changed_synergy | 1 |
| assets/changed_synergy/lang | 4 |
| assets/changed_synergy/models | 2 |
| assets/changed_synergy/shaders | 1 |
| assets/changed_synergy/textures | 25 |
| assets/minecraft | 0 |
| assets/minecraft/shaders | 3 |
| assets/zzz_changed_synergy | 0 |
| assets/zzz_changed_synergy/lang | 1 |
| data | 0 |
| data/changed | 0 |
| data/changed/tags | 2 |
| data/changed/worldgen | 2 |
| data/changed_synergy | 0 |
| data/changed_synergy/advancements | 29 |
| data/changed_synergy/curios | 4 |
| data/changed_synergy/forge | 12 |
| data/changed_synergy/latex_fusions | 1 |
| data/changed_synergy/recipes | 1 |
| data/changed_synergy/settlement_blueprints | 14 |
| data/changed_synergy/tags | 48 |
| data/changed_synergy/worldgen | 39 |
| data/forge | 0 |
| data/forge/tags | 1 |
| data/minecraft | 0 |
| data/minecraft/tags | 2 |

## 10. Known risks (from KNOWN_ISSUES.md + survey)
- Tightly pinned to Changed 0.15.7 ([0.15.7,0.15.8)); a small upstream update can break a mixin.
- Large mixin surface with defaultRequire=1; one stale target crashes startup.
- God classes in `ai/` and `event/` (see Hotspots); splitting them is the main maintainability win.
- No automated in-game test suite; only tools/tests/FactionDiplomacyTest.java exists.
- Behavior is spread across ai/, event/, mixin/ and compat/; one feature (e.g. takeover, hypnosis) touches all four.

## 11. PLAN (edit me)
1. Snapshot: branch `upstream-snapshot` untouched; work on `lts/main`.
2. Decide identity: new mod_id/name vs keep (see section 5) and publish naming so it cannot clash with upstream.
3. Decide target: stay Forge 1.20.1 for the LTS, or port (NeoForge/newer MC) first.
4. Get a clean build + run configuration working before changing behavior.
5. Triage per-file table: mark each keep / rewrite / drop; start with the Hotspots.
6. Add tests around persistence, packets, and relationship transitions before rewriting them.
7. Rewrite by feature slice (takeover, hypnosis, settlements, ...), each slice owning its ai/event/mixin/client files.

## 12. Per-file table
| Path | Lines | Role | Verdict (keep/rewrite/drop) | Notes |
| --- | --- | --- | --- | --- |
| ChangedSynergyClientConfig.java | 124 | model/util | ? |  |
| ChangedSynergyConfig.java | 432 | model/util | ? |  |
| ChangedSynergyMod.java | 68 | model/util | ? |  |
| advancement/SynergyAdvancements.java | 61 | model/util | ? |  |
| ai/AddonCarriedPlayerMotionGuard.java | 20 | model/util | ? |  |
| ai/AggressiveMercyService.java | 104 | service | ? |  |
| ai/BondReleaseService.java | 60 | service | ? |  |
| ai/BondedCreatureDeathData.java | 95 | saved-data | ? |  |
| ai/BondedCreatureLifecycle.java | 369 | model/util | ? |  |
| ai/BondedCreatureReleaseData.java | 87 | saved-data | ? |  |
| ai/BondedEmergencySuitGoal.java | 160 | ai-goal | ? |  |
| ai/BondedFollowGoal.java | 149 | ai-goal | ? |  |
| ai/BondedOwnerDefenseGoal.java | 136 | ai-goal | ? |  |
| ai/BondedOwnerGrabRescueGoal.java | 246 | ai-goal | ? |  |
| ai/BondedPetSettings.java | 242 | state | ? |  |
| ai/BondedRevivalData.java | 118 | saved-data | ? |  |
| ai/BondedRevivalService.java | 632 | service | ? |  |
| ai/BondedShoreWaitGoal.java | 37 | ai-goal | ? |  |
| ai/BondedSuitDimensionTransfer.java | 99 | model/util | ? |  |
| ai/BondedSuitService.java | 1008 | service | ? |  |
| ai/BondedTeleportSafety.java | 383 | model/util | ? |  |
| ai/CacheGuardReturnGoal.java | 90 | ai-goal | ? |  |
| ai/CompanionFollowNavigation.java | 199 | model/util | ? |  |
| ai/CompanionWorkDialogue.java | 145 | model/util | ? |  |
| ai/CreatureArmorService.java | 207 | service | ? |  |
| ai/CreatureCacheGuardService.java | 480 | service | ? |  |
| ai/CreatureComfortGoal.java | 559 | ai-goal | ? |  |
| ai/CreatureCommunityData.java | 968 | saved-data | ? |  |
| ai/CreatureIdentity.java | 752 | model/util | ? |  |
| ai/CreatureLifeMemory.java | 332 | state | ? |  |
| ai/CreatureMorphAliasData.java | 98 | saved-data | ? |  |
| ai/CreatureMorphContinuity.java | 202 | model/util | ? |  |
| ai/CreaturePersonality.java | 1148 | model/util | ? |  |
| ai/CreatureRelationshipForgetData.java | 65 | saved-data | ? |  |
| ai/CreatureRoleService.java | 225 | service | ? |  |
| ai/CreatureRoutineGoal.java | 989 | ai-goal | ? |  |
| ai/CreatureSettlementService.java | 4348 | service | ? |  |
| ai/CreatureSocialProfile.java | 161 | state | ? |  |
| ai/DarkLatexDisguise.java | 227 | model/util | ? |  |
| ai/EquipmentInheritance.java | 152 | model/util | ? |  |
| ai/ExoskeletonTakeoverAdapter.java | 647 | model/util | ? |  |
| ai/FactionDiplomacy.java | 58 | model/util | ? |  |
| ai/FactionHostilityGrace.java | 193 | model/util | ? |  |
| ai/FactionPursuitService.java | 262 | service | ? |  |
| ai/FactionReputation.java | 559 | model/util | ? |  |
| ai/FallbackBondedTargetGoal.java | 43 | ai-goal | ? |  |
| ai/FallbackBondedWorkGoal.java | 447 | ai-goal | ? |  |
| ai/FirearmEvasionGoal.java | 112 | ai-goal | ? |  |
| ai/FirearmThreatService.java | 156 | service | ? |  |
| ai/FishingVisualEffects.java | 223 | model/util | ? |  |
| ai/FlyingLatexGlideService.java | 85 | service | ? |  |
| ai/GatheringToolPresentation.java | 110 | model/util | ? |  |
| ai/GrabEscapeStunService.java | 118 | service | ? |  |
| ai/HumanBoundaryService.java | 161 | service | ? |  |
| ai/HumanIntent.java | 96 | model/util | ? |  |
| ai/HuntMemory.java | 160 | state | ? |  |
| ai/HuntState.java | 9 | state | ? |  |
| ai/HunterArchetype.java | 114 | model/util | ? |  |
| ai/HunterFaction.java | 181 | model/util | ? |  |
| ai/HunterRelation.java | 44 | model/util | ? |  |
| ai/HypnosisFocusGoal.java | 52 | ai-goal | ? |  |
| ai/HypnosisGazeContest.java | 59 | model/util | ? |  |
| ai/HypnosisProfile.java | 78 | state | ? |  |
| ai/HypnosisQteService.java | 810 | service | ? |  |
| ai/InheritedEyeAppearance.java | 100 | model/util | ? |  |
| ai/InvoluntaryTransfurNegotiation.java | 2612 | model/util | ? |  |
| ai/LatexCreatureCombatRules.java | 273 | model/util | ? |  |
| ai/LatexFusionIntent.java | 203 | model/util | ? |  |
| ai/LatexSocialMemory.java | 1896 | state | ? |  |
| ai/LatexSocialRelation.java | 247 | model/util | ? |  |
| ai/LightFactionGroup.java | 192 | model/util | ? |  |
| ai/MergedPlayerIdentity.java | 155 | model/util | ? |  |
| ai/OrganicCombatRules.java | 114 | model/util | ? |  |
| ai/PatAnimationService.java | 358 | service | ? |  |
| ai/PlayerOutpostData.java | 299 | saved-data | ? |  |
| ai/PlayerOutpostGoal.java | 454 | ai-goal | ? |  |
| ai/PlayerOutpostRestGoal.java | 180 | ai-goal | ? |  |
| ai/PlayerOutpostService.java | 254 | service | ? |  |
| ai/PlayerOutpostSupplyType.java | 29 | model/util | ? |  |
| ai/PlayerRelationshipSettings.java | 414 | state | ? |  |
| ai/PoliteHumanApproachGoal.java | 203 | ai-goal | ? |  |
| ai/PoliteHumanInteraction.java | 401 | model/util | ? |  |
| ai/ProvisionerFishingFocus.java | 102 | model/util | ? |  |
| ai/ProvisionerGiftService.java | 428 | service | ? |  |
| ai/ProvisionerTradeService.java | 785 | service | ? |  |
| ai/PureWhiteReformationGoal.java | 260 | ai-goal | ? |  |
| ai/PureWhiteWolfAdaptation.java | 218 | model/util | ? |  |
| ai/RelationshipFavorService.java | 384 | service | ? |  |
| ai/ReleasePlacementService.java | 158 | service | ? |  |
| ai/SafeEntityMutationQueue.java | 62 | model/util | ? |  |
| ai/SharedRestGoal.java | 290 | ai-goal | ? |  |
| ai/SmartSearchGoal.java | 167 | ai-goal | ? |  |
| ai/SocialAudienceGoal.java | 186 | ai-goal | ? |  |
| ai/SocialFollowGoal.java | 146 | ai-goal | ? |  |
| ai/SocialFriendDefenseGoal.java | 339 | ai-goal | ? |  |
| ai/SynergyPatService.java | 67 | service | ? |  |
| ai/TakeoverAssimilationBehavior.java | 72 | model/util | ? |  |
| ai/TakeoverConflictMemory.java | 64 | state | ? |  |
| ai/TakeoverSafety.java | 149 | model/util | ? |  |
| ai/TakeoverService.java | 1714 | service | ? |  |
| ai/TakeoverSession.java | 473 | model/util | ? |  |
| ai/TakeoverSessionNbt.java | 132 | model/util | ? |  |
| ai/TelepathyService.java | 94 | service | ? |  |
| ai/UnderwaterPursuitGoal.java | 203 | ai-goal | ? |  |
| ai/VoluntaryBondTransfurService.java | 202 | service | ? |  |
| api/ChangedSynergyApi.java | 47 | model/util | ? |  |
| api/SynergyMerchantMenuMarker.java | 7 | model/util | ? |  |
| client/AbsorptionNegotiationClientState.java | 35 | client | ? |  |
| client/AbsorptionPreviewRenderState.java | 33 | client | ? |  |
| client/BondedCreatureInventoryScreen.java | 182 | client | ? |  |
| client/BondedLatexScreen.java | 356 | client | ? |  |
| client/BondedWheelSwitchClientEvents.java | 54 | client | ? |  |
| client/CentaurMountConfigScreen.java | 134 | client | ? |  |
| client/CentaurMountHintOverlay.java | 71 | client | ? |  |
| client/ChangedSynergyConfigScreen.java | 765 | client | ? |  |
| client/ChangedSynergyEntityRenderers.java | 27 | client | ? |  |
| client/ChangedSynergyScreens.java | 78 | client | ? |  |
| client/CreatureFishingHookRenderer.java | 165 | client | ? |  |
| client/EmoteClientState.java | 70 | client | ? |  |
| client/FriendlySuitClientState.java | 179 | client | ? |  |
| client/FriendlySuitVignetteOverlay.java | 60 | client | ? |  |
| client/FriendlyWrapMaskRenderer.java | 231 | client | ? |  |
| client/GrabQteClientState.java | 98 | client | ? |  |
| client/GrabQteOverlayRenderer.java | 573 | client | ? |  |
| client/HumanPlayerPreviewRenderState.java | 25 | client | ? |  |
| client/HypnosisQteAnimationState.java | 67 | client | ? |  |
| client/HypnosisQteClientState.java | 427 | client | ? |  |
| client/HypnosisQteOverlay.java | 584 | client | ? |  |
| client/LegacyTransfurProgressLayer.java | 114 | client | ? |  |
| client/LegacyTransfurVisualState.java | 81 | client | ? |  |
| client/LegacyTransfurVisuals.java | 101 | client | ? |  |
| client/MechanicHintClientEvents.java | 209 | client | ? |  |
| client/MergedPlayerIdentityClient.java | 45 | client | ? |  |
| client/NameVisibilityClientEvents.java | 34 | client | ? |  |
| client/NativePetRadialClientEvents.java | 115 | client | ? |  |
| client/OrganicTransfurMaskRenderer.java | 169 | client | ? |  |
| client/PatAnimationClientState.java | 195 | client | ? |  |
| client/PatInputClientEvents.java | 120 | client | ? |  |
| client/PerformanceDiagnosticsClient.java | 80 | client | ? |  |
| client/PlayerOutpostHintOverlay.java | 48 | client | ? |  |
| client/PlayerOutpostScreen.java | 195 | client | ? |  |
| client/PlayerRelationshipClientEvents.java | 140 | client | ? |  |
| client/PlayerRelationshipScreen.java | 634 | client | ? |  |
| client/ProvisionerTradeScreen.java | 323 | client | ? |  |
| client/PureWhiteBlindnessOverlayGuard.java | 52 | client | ? |  |
| client/PureWhiteVisionClientModEvents.java | 26 | client | ? |  |
| client/PureWhiteVisionClientState.java | 136 | client | ? |  |
| client/PureWhiteVisionRenderer.java | 201 | client | ? |  |
| client/QteAnimationUtil.java | 89 | client | ? |  |
| client/RadialWheelAnimationAccess.java | 13 | client | ? |  |
| client/RadialWheelAnimations.java | 192 | client | ? |  |
| client/RevivalGrabAbilityClient.java | 51 | client | ? |  |
| client/ScoutTargetClientState.java | 60 | client | ? |  |
| client/SocialInteractionScreen.java | 771 | client | ? |  |
| client/SynergyKeyMappings.java | 32 | client | ? |  |
| client/TaczClientInputBlocker.java | 109 | client | ? |  |
| client/TakeoverClientState.java | 564 | client | ? |  |
| client/TakeoverOverlay.java | 246 | client | ? |  |
| client/TakeoverScreen.java | 177 | client | ? |  |
| client/TaurRiderLeanClientState.java | 230 | client | ? |  |
| client/TelepathyDanmakuOverlay.java | 425 | client | ? |  |
| client/TelepathyDanmakuState.java | 122 | client | ? |  |
| client/TerritoryClientState.java | 535 | client | ? |  |
| client/TerritoryHudOverlay.java | 217 | client | ? |  |
| client/WhiteHiveTargetClientState.java | 36 | client | ? |  |
| command/BondCommand.java | 621 | command | ? |  |
| command/PersonalitySpawnCommand.java | 93 | command | ? |  |
| command/PlayerOutpostCommand.java | 288 | command | ? |  |
| command/ServerConfigCommand.java | 199 | command | ? |  |
| compat/ChangedAddonCompat.java | 294 | compat | ? |  |
| compat/ChangedExtrasCompat.java | 225 | compat | ? |  |
| compat/ChangedVanillaCompat.java | 112 | compat | ? |  |
| compat/DomesticationInnovationCompat.java | 91 | compat | ? |  |
| compat/FirearmCompat.java | 309 | compat | ? |  |
| compat/TrueTransfurCompat.java | 67 | compat | ? |  |
| compat/addon/AddonAnimalCalls.java | 57 | compat | ? |  |
| compat/addon/ChangedAddonSocialEvents.java | 1278 | compat | ? |  |
| compat/addon/HostileTransfurredGrabGoal.java | 317 | compat | ? |  |
| compat/addon/OrganicAssimilationGrabGoal.java | 332 | compat | ? |  |
| compat/addon/OrganicOwnerEvacuationGoal.java | 422 | compat | ? |  |
| compat/addon/SocialGrabDamageGoal.java | 116 | compat | ? |  |
| compat/addon/SocialMayDropGrabbedEntityGoal.java | 35 | compat | ? |  |
| compat/addon/SocialMayGrabTargetGoal.java | 72 | compat | ? |  |
| compat/curios/CuriosApiBridge.java | 138 | compat | ? |  |
| compat/curios/CuriosCompat.java | 96 | compat | ? |  |
| dialogue/FacilityArea.java | 131 | dialogue | ? |  |
| dialogue/LatexTerritory.java | 431 | dialogue | ? |  |
| dialogue/NpcDialogue.java | 1714 | dialogue | ? |  |
| dialogue/NpcEmoteState.java | 210 | dialogue | ? |  |
| effect/MesmerizedEffect.java | 29 | model/util | ? |  |
| entity/CreatureFishingHookVisual.java | 91 | model/util | ? |  |
| event/AssimilationEcologyEvents.java | 125 | events | ? |  |
| event/BondedRevivalEvents.java | 204 | events | ? |  |
| event/CreatureCacheGuardEvents.java | 47 | events | ? |  |
| event/DarkLatexDisguiseEvents.java | 144 | events | ? |  |
| event/FactionReputationEvents.java | 555 | events | ? |  |
| event/HuntAIEvents.java | 1111 | events | ? |  |
| event/LatexNaturalSpawnBalancer.java | 48 | events | ? |  |
| event/LatexSocialEvents.java | 2251 | events | ? |  |
| event/NpcDispositionEvents.java | 320 | events | ? |  |
| event/OrganicEvacuationEvents.java | 45 | events | ? |  |
| event/PlayerOrangeHarvestEvents.java | 91 | events | ? |  |
| event/PureWhiteHiveEvents.java | 228 | events | ? |  |
| event/RandomizedTransfurMethodEvents.java | 126 | events | ? |  |
| event/TelepathyEvents.java | 43 | events | ? |  |
| event/TerritoryContextEvents.java | 393 | events | ? |  |
| event/TransfurVisualEvents.java | 232 | events | ? |  |
| event/WrappedSleepEvents.java | 101 | events | ? |  |
| init/ChangedSynergyEntities.java | 34 | registry | ? |  |
| init/ChangedSynergyGameRules.java | 75 | registry | ? |  |
| init/ChangedSynergyItems.java | 29 | registry | ? |  |
| init/ChangedSynergyMenus.java | 57 | registry | ? |  |
| init/ChangedSynergyMobEffects.java | 20 | registry | ? |  |
| init/ChangedSynergyRecipeSerializers.java | 23 | registry | ? |  |
| init/ChangedSynergySoundEvents.java | 33 | registry | ? |  |
| item/BrokenDarkLatexMaskItem.java | 35 | model/util | ? |  |
| item/RepairedDarkLatexMaskItem.java | 11 | model/util | ? |  |
| mixin/AbilityRadialNegotiationMixin.java | 129 | mixin | ? |  |
| mixin/AbilityRadialScreenCloseMixin.java | 27 | mixin | ? |  |
| mixin/AddonAlphaLeapGrabMixin.java | 31 | mixin | ? |  |
| mixin/AddonCarryMountPoseMixin.java | 34 | mixin | ? |  |
| mixin/AddonNativeSuitGoalGuardMixin.java | 30 | mixin | ? |  |
| mixin/AddonThunderDashCarryMixin.java | 27 | mixin | ? |  |
| mixin/AddonThunderDiveCarryMixin.java | 29 | mixin | ? |  |
| mixin/AquaticGoToWaterRoutineMixin.java | 41 | mixin | ? |  |
| mixin/BeehivePlacementMixin.java | 51 | mixin | ? |  |
| mixin/BetterCombatFriendlyWrapTargetMixin.java | 38 | mixin | ? |  |
| mixin/BondedInfuserRecipeMixin.java | 52 | mixin | ? |  |
| mixin/BondedRevivalVesselUseMixin.java | 26 | mixin | ? |  |
| mixin/CentaurControllingPassengerMixin.java | 36 | mixin | ? |  |
| mixin/CentaurHorseInterfaceMixin.java | 51 | mixin | ? |  |
| mixin/CentaurRideControlMixin.java | 131 | mixin | ? |  |
| mixin/ChangedEntityAbilityInvoker.java | 15 | mixin | ? |  |
| mixin/ChangedEntityAiTimingMixin.java | 39 | mixin | ? |  |
| mixin/ChangedEntityInheritedEyesMixin.java | 36 | mixin | ? |  |
| mixin/ChangedEntityPatPoseMixin.java | 30 | mixin | ? |  |
| mixin/ChangedExtrasLatexBrainMixin.java | 52 | mixin | ? |  |
| mixin/ChangedExtrasSmartAiHandlerMixin.java | 51 | mixin | ? |  |
| mixin/ChangedKeepConsciousDefaultMixin.java | 41 | mixin | ? |  |
| mixin/DarkLatexWolfPupAgeAccessor.java | 16 | mixin | ? |  |
| mixin/DarkLatexWolfPupMorphMixin.java | 49 | mixin | ? |  |
| mixin/DomesticationInnovationTameableUtilsMixin.java | 80 | mixin | ? |  |
| mixin/EmoteParticleMixin.java | 56 | mixin | ? |  |
| mixin/ExoskeletonRestrainTakeoverMixin.java | 67 | mixin | ? |  |
| mixin/ExoskeletonTakeoverItemStateMixin.java | 19 | mixin | ? |  |
| mixin/FiniteEntityPushMixin.java | 20 | mixin | ? |  |
| mixin/FriendlyLatexSleepMixin.java | 36 | mixin | ? |  |
| mixin/GrabAssimilationModeMixin.java | 50 | mixin | ? |  |
| mixin/GrabOverlayAnimationMixin.java | 80 | mixin | ? |  |
| mixin/GrabQteSyncMixin.java | 286 | mixin | ? |  |
| mixin/HeldCreaturePositionMixin.java | 34 | mixin | ? |  |
| mixin/HumanPlayerPreviewMixin.java | 29 | mixin | ? |  |
| mixin/HurtByTargetGoalNullGuardMixin.java | 36 | mixin | ? |  |
| mixin/HypnosisAbilityMixin.java | 20 | mixin | ? |  |
| mixin/HypnosisCameraGuardMixin.java | 29 | mixin | ? |  |
| mixin/HypnosisChangedEntityAttackGuardMixin.java | 34 | mixin | ? |  |
| mixin/HypnosisClientCameraGuardMixin.java | 31 | mixin | ? |  |
| mixin/HypnosisClientControlMixin.java | 52 | mixin | ? |  |
| mixin/HypnosisClientEffectGuardMixin.java | 37 | mixin | ? |  |
| mixin/HypnosisEffectGuardMixin.java | 53 | mixin | ? |  |
| mixin/HypnosisKeyboardControlMixin.java | 33 | mixin | ? |  |
| mixin/HypnosisMobAttackGuardMixin.java | 34 | mixin | ? |  |
| mixin/HypnosisMouseControlMixin.java | 51 | mixin | ? |  |
| mixin/HypnosisMovementInputMixin.java | 36 | mixin | ? |  |
| mixin/LabTablePathfindingMixin.java | 32 | mixin | ? |  |
| mixin/MonsterDaylightSpawnMixin.java | 31 | mixin | ? |  |
| mixin/NativeRadialFrameAlphaMixin.java | 43 | mixin | ? |  |
| mixin/NonEntityMerchantSoundMixin.java | 26 | mixin | ? |  |
| mixin/OrganicEvacuationDropGuardMixin.java | 61 | mixin | ? |  |
| mixin/OrganicTransfurRestrictionMixin.java | 77 | mixin | ? |  |
| mixin/OverworldBiomeBuilderMixin.java | 81 | mixin | ? |  |
| mixin/PinkShortsAccessoryTickMixin.java | 17 | mixin | ? |  |
| mixin/PlayerPatPoseMixin.java | 29 | mixin | ? |  |
| mixin/RadialScreenAnimationMixin.java | 779 | mixin | ? |  |
| mixin/RandomizedTransfurDecisionMixin.java | 24 | mixin | ? |  |
| mixin/RelationshipPeacefulDespawnMixin.java | 45 | mixin | ? |  |
| mixin/RepairedDarkLatexMaskLayerMixin.java | 41 | mixin | ? |  |
| mixin/SharedRestCameraMixin.java | 31 | mixin | ? |  |
| mixin/SocialMobCombatGuardMixin.java | 51 | mixin | ? |  |
| mixin/SocialTargetGuardMixin.java | 80 | mixin | ? |  |
| mixin/SpawnPlacementsDaylightContextMixin.java | 40 | mixin | ? |  |
| mixin/SurfaceSystemMixin.java | 45 | mixin | ? |  |
| mixin/TaczAdditionsSuitGunTuckMixin.java | 31 | mixin | ? |  |
| mixin/TakeoverAbilityPacketMixin.java | 26 | mixin | ? |  |
| mixin/TakeoverAbsorptionMixin.java | 63 | mixin | ? |  |
| mixin/TakeoverExtraJumpPacketMixin.java | 31 | mixin | ? |  |
| mixin/TakeoverGrabMixin.java | 140 | mixin | ? |  |
| mixin/TakeoverHypnosisIsolationMixin.java | 39 | mixin | ? |  |
| mixin/TakeoverKeyboardMixin.java | 30 | mixin | ? |  |
| mixin/TakeoverLocalPlayerMixin.java | 17 | mixin | ? |  |
| mixin/TakeoverMinecraftMixin.java | 26 | mixin | ? |  |
| mixin/TakeoverMouseMixin.java | 45 | mixin | ? |  |
| mixin/TakeoverMovementInputMixin.java | 21 | mixin | ? |  |
| mixin/TakeoverNativeServerPacketMixin.java | 53 | mixin | ? |  |
| mixin/TakeoverPlayerAbsorptionMixin.java | 49 | mixin | ? |  |
| mixin/TakeoverServerInputMixin.java | 45 | mixin | ? |  |
| mixin/TakeoverUntransfurCommandMixin.java | 28 | mixin | ? |  |
| mixin/TaurChestPackNpcMixin.java | 32 | mixin | ? |  |
| mixin/TransfurVariantInstanceInheritedEyesMixin.java | 56 | mixin | ? |  |
| mixin/VanillaOakFoliageMixin.java | 46 | mixin | ? |  |
| mixin/VariantAbilityActivateMixin.java | 70 | mixin | ? |  |
| mixin/WhiteHiveTargetColorMixin.java | 45 | mixin | ? |  |
| mixin/WhiteHiveTargetGlowMixin.java | 45 | mixin | ? |  |
| mixin/WhiteLatexPillarContactMixin.java | 97 | mixin | ? |  |
| mixin/WhiteLatexTerritorySpawnMixin.java | 97 | mixin | ? |  |
| network/AbsorptionNegotiationStatePacket.java | 34 | packet | ? |  |
| network/BondedInventoryOpenPacket.java | 37 | packet | ? |  |
| network/ChangedSynergyNetwork.java | 203 | network | ? |  |
| network/EmoteTransitionPacket.java | 46 | packet | ? |  |
| network/ExoskeletonMotionPacket.java | 36 | packet | ? |  |
| network/FriendlySocialHugState.java | 54 | network | ? |  |
| network/FriendlySocialHugSyncPacket.java | 42 | packet | ? |  |
| network/FriendlySuitSyncPacket.java | 38 | packet | ? |  |
| network/GrabQteSyncPacket.java | 44 | packet | ? |  |
| network/HypnosisQteSyncPacket.java | 51 | packet | ? |  |
| network/MergedPlayerIdentityPacket.java | 40 | packet | ? |  |
| network/NativePetReassimilatePacket.java | 37 | packet | ? |  |
| network/OpenAbsorptionNegotiationPacket.java | 51 | packet | ? |  |
| network/PatAnimationControlPacket.java | 54 | packet | ? |  |
| network/PatAnimationPacket.java | 42 | packet | ? |  |
| network/PatAnimationSpeedPacket.java | 32 | packet | ? |  |
| network/PerformanceSnapshotPacket.java | 49 | packet | ? |  |
| network/PlayerRelationshipOpenPacket.java | 37 | packet | ? |  |
| network/ProvisionerTradeSyncPacket.java | 51 | packet | ? |  |
| network/RevivalGrabAbilityPacket.java | 24 | packet | ? |  |
| network/ScoutTargetPacket.java | 33 | packet | ? |  |
| network/TakeoverActionPacket.java | 34 | packet | ? |  |
| network/TakeoverStatePacket.java | 55 | packet | ? |  |
| network/TelepathyDialoguePacket.java | 48 | packet | ? |  |
| network/TerritorySyncPacket.java | 64 | packet | ? |  |
| network/TransfurVisualPacket.java | 33 | packet | ? |  |
| network/WhiteHiveTargetsPacket.java | 48 | packet | ? |  |
| performance/SynergyPerformanceTracker.java | 231 | model/util | ? |  |
| recipe/RevivalMaskRepairRecipe.java | 66 | model/util | ? |  |
| util/PureWhiteVision.java | 20 | model/util | ? |  |
| world/ChangedSpawnPlacementContext.java | 64 | model/util | ? |  |
| world/CreatureSettlementBlueprints.java | 265 | model/util | ? |  |
| world/LatexTerritoryBiomes.java | 40 | model/util | ? |  |
| world/OrangeLeafRegrowthData.java | 173 | saved-data | ? |  |
| world/inventory/BondedCreatureInventory.java | 280 | menu | ? |  |
| world/inventory/BondedCreatureInventoryMenu.java | 799 | menu | ? |  |
| world/inventory/BondedInventoryService.java | 97 | menu | ? |  |
| world/inventory/BondedLatexMenu.java | 306 | menu | ? |  |
| world/inventory/CentaurMountCargo.java | 98 | menu | ? |  |
| world/inventory/CentaurMountConfigMenu.java | 325 | menu | ? |  |
| world/inventory/CentaurMountService.java | 284 | menu | ? |  |
| world/inventory/PlayerOutpostMenu.java | 213 | menu | ? |  |
| world/inventory/PlayerRelationshipMenu.java | 649 | menu | ? |  |
| world/inventory/ProvisionerTradeMenu.java | 206 | menu | ? |  |
| world/inventory/SocialInteractionMenu.java | 1191 | menu | ? |  |
