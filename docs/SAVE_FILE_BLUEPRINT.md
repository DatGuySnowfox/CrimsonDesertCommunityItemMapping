# Crimson Desert Save File — Complete Blueprint

Generated from two game-produced zero-item saves:
- **Early game**: 2,289,946 bytes, 54 types, 23 blocks
- **Endgame** (all quests done): 4,211,068 bytes, 88 types, 899 blocks

Every byte in these saves was written by the game itself — this is the definitive reference.

## 1. Binary Layout
```
[FF FF 04 00]  Magic (4 bytes)
[Schema]       Type definitions (variable size)
[TOC Header]   zero(u32) + entry_count(u32) + stream_size(u32)  (12 bytes)
[TOC Entries]  entry_count × 20 bytes each:
                 class_index(u32) + sentinel(u32=FFFFFFFF) + sentinel(u32=FFFFFFFF)
                 + data_offset(u32) + data_size(u32)
[Block 0]      Object data
[Block 1]      ...
[Block N]      Contiguous, no gaps
```

## 2. Crypto Pipeline
```
File → Header(0x80) → ChaCha20 decrypt → HMAC-SHA256 verify → LZ4 decompress → PARC blob
PARC blob → LZ4-HC compress → HMAC-SHA256 → ChaCha20 encrypt → Header + payload → File

Header (0x80 bytes):
  +0x00  "SAVE" magic (4B)
  +0x04  version u16 = 2
  +0x06  flags u16 = 0x0080
  +0x12  uncompressed_size u32
  +0x16  compressed_size u32
  +0x1A  nonce (16 bytes: counter_u32_LE + nonce_12B)
  +0x2A  HMAC-SHA256 (32 bytes)
  +0x4A  reserved zeros (54 bytes)
  +0x80  encrypted payload begins

Key: 9a4beb127f9e748b148d6690c25cc9379a315bd56c28af6319fd559f1152ac00
```

## 3. Complete Schema (88 types)

### [ 0] CharacterStatusSaveData (8 fields)
  - `_characterKey`: CharacterKey [scalar, 4B]
  - `_factionKey`: FactionKey [scalar, 4B]
  - `_level`: TLevel [scalar, 4B]
  - `_experience`: TExperience [scalar, 8B]
  - `_remainExperience`: TExperience [scalar, 8B]
  - `_remainSkillPoint`: TSkillPoint [scalar, 2B]
  - `_currentHp`: TStat [scalar, 8B]
  - `_currentMp`: TStat [scalar, 8B]

### [ 1] FieldNPCSaveData (8 fields) *(endgame only)*
  - `_spawnFieldInfoKey`: FieldInfoKey [scalar, 4B]
  - `_fieldNpcSaveDataKey`: FieldNPCSaveDataKey [scalar, 4B]
  - `_friendly`: ReflectObject [ReflectObj, 8B]
  - `_nudeAppearanceIndexKey`: CharacterAppearanceIndexKey [scalar, 8B]
  - `_customizationAppearanceIndexKey`: CharacterAppearanceIndexKey [scalar, 8B]
  - `_armorDyeAppearanceIndexKey`: uint8 [scalar, 1B]
  - `_characterKey`: CharacterKey [scalar, 4B]
  - `_touchID`: uint64 [scalar, 8B]

### [ 2] CustomizationSaveData (3 fields) *(endgame only)*
  - `_meshData`: uint8 [scalar_list, 1B]
  - `_decorationData`: uint8 [scalar_list, 1B]
  - `_version`: uint32 [scalar, 4B]

### [ 3] NPCScheduleCharacterSaveData (4 fields) *(endgame only)*
  - `_fieldCharacterSaveData`: ReflectObject [ReflectObj, 8B]
  - `_npcScheduleKeyIndex`: uint32 [scalar, 4B]
  - `_nodeId`: uint32 [scalar, 4B]
  - `_isRetreatBySpawnRate`: bool [scalar, 1B]

### [ 4] FieldGimmickSaveData_AutoSpawnOwnerData (4 fields)
  - `_isMainAutoSpawnActor`: bool [scalar, 1B]
  - `_spawningPoolAutoSpawnInfoKey`: SpawningPoolAutoSpawnInfoKey [scalar, 4B]
  - `_spawningPoolSceneObjectUuid`: uint4 [scalar, 16B]
  - `_spawningPoolSocketName`: IndexedStringA [string/bytes, 1B]

### [ 5] MissionStateData (12 fields)
  - `_key`: MissionKey [scalar, 4B]
  - `_state`: QuestStateType [enum, 1B]
  - `_uiState`: MissionUIState [enum, 1B]
  - `_branchedTime`: uint64 [scalar, 8B]
  - `_completedTime`: uint64 [scalar, 8B]
  - `_delayedTime`: uint64 [scalar, 8B]
  - `_delayedFromMissionKey`: MissionKey [scalar, 4B]
  - `_uiPosition`: float3 [scalar, 12B]
  - `_usedTagList`: StringInfoKey [scalar_list, 4B]
  - `_completeCount`: uint32 [scalar, 4B]
  - `_overlapTargetList`: uint64 [scalar_list, 8B]
  - `_newAlarm`: bool [scalar, 1B]

### [ 6] QuestGaugeStateData_Stage (3 fields) *(endgame only)*
  - `_key`: StageKey [scalar, 4B]
  - `_killRatio`: float [scalar, 4B]
  - `_deadCount_deprecated`: uint16 [scalar, 2B]

### [ 7] SubLevelElementSaveData (4 fields) *(endgame only)*
  - `_key`: SubLevelKey [scalar, 4B]
  - `_maxAchievedLevel`: TLevel [scalar, 4B]
  - `_level`: TLevel [scalar, 4B]
  - `_experience`: TExperience [scalar, 8B]

### [ 8] SubLevelSaveData (2 fields)
  - `_list`: ReflectObject [ObjList, 0B]
  - `_experienceByDonationDataList`: ReflectObject [ObjList, 0B]

### [ 9] ExecutedGameAdviceInfoKeySaveData (1 fields) *(endgame only)*
  - `_key`: GameAdviceInfoKey [scalar, 4B]

### [10] ItemSaveData (22 fields)
  - `_saveVersion`: uint32 [scalar, 4B]
  - `_itemNo`: ItemNo [scalar, 8B]
  - `_itemKey`: ItemKey [scalar, 4B]
  - `_slotNo`: TItemSlotNo [scalar, 2B]
  - `_stackCount`: TStackCount [scalar, 8B]
  - `_enchantLevel`: TEnchantLevel [scalar, 2B]
  - `_useableCtc`: Ctc64 [scalar, 8B]
  - `_endurance`: TEndurance [scalar, 2B]
  - `_sharpness`: TEndurance [scalar, 2B]
  - `_batteryStat`: TStat [scalar, 8B]
  - `_maxBatteryStat`: TStat [scalar, 8B]
  - `_maxSocketCount`: TSocketSlotNo [scalar, 1B]
  - `_validSocketCount`: TSocketSlotNo [scalar, 1B]
  - `_socketSaveDataList`: ReflectObject [ObjList, 0B]
  - `_itemDyeDataList`: ReflectObject [ObjList, 0B]
  - `_dropResultSubSaveItemList`: ReflectObject [ObjList, 0B]
  - `_transferredItemKey`: ItemKey [scalar, 4B]
  - `_currentGimmickState`: HashCode32 [scalar, 4B]
  - `_chargedUseableCount`: TickCount64 [scalar, 8B]
  - `_timeWhenPushItem`: Ctc64 [scalar, 8B]
  - `_characterConversionData`: ReflectObjectPtr [ReflectObjPtr, 8B]
  - `_isNewMark`: bool [scalar, 1B]

### [11] GameEventSaveData (1 fields)
  - `_list`: GameEventHandlerKey [scalar_list, 2B]

### [12] NPCScheduleStageManagerSaveData (1 fields)
  - `_stageList`: ReflectObject [ObjList, 0B]

### [13] EquipmentSaveData (4 fields)
  - `_equipCacheSequenceNo`: TCacheSequenceNo [scalar, 4B]
  - `_lastEquipShieldItemKey`: ItemKey [scalar, 4B]
  - `_list`: ReflectObject [ObjList, 0B]
  - `_useItemSaveList`: ReflectObject [ObjList, 0B]

### [14] StoreDataSaveData (6 fields)
  - `_storeKey`: StoreKey [scalar, 2B]
  - `_lastPriceRefreshFieldTime`: uint64 [scalar, 8B]
  - `_storeItemList`: ReflectObject [ObjList, 0B]
  - `_storeSoldItemDataList`: ReflectObject [ObjList, 0B]
  - `_itemSoldFieldTimeRawList`: uint64 [scalar_list, 8B]
  - `_storeSoldGimmickSaveDataList`: ReflectObject [ObjList, 0B]

### [15] UseItemReserveSlotElementSaveData (15 fields)
  - `_specialNameKey`: StringInfoKey [scalar, 4B]
  - `_inventoryType`: InventoryKey [scalar, 2B]
  - `_inventorySlotNo`: TInventorySlotNo [scalar, 2B]
  - `_useItemReserveSlotKey`: ReserveSlotKey [scalar, 4B]
  - `_vehicleMercenaryNo`: MercenaryNo [scalar, 8B]
  - `_reserveSkillKey`: SkillKey [scalar, 4B]
  - `_reserveStatusKey`: StatusKey [scalar, 4B]
  - `_reserveItemGroupKey`: ItemGroupKey [scalar, 2B]
  - `_reserveItemNo`: ItemNo [scalar, 8B]
  - `_itemKey`: ItemKey [scalar, 4B]
  - `_equipSlotNo`: TEquipSlotNo [scalar, 2B]
  - `_enchantLevel`: TEnchantLevel [scalar, 2B]
  - `_isUseFakeEquipStat`: bool [scalar, 1B]
  - `_isUseFakeEquipMesh`: bool [scalar, 1B]
  - `_reserveItem`: ReflectObject [ReflectObj, 8B]

### [16] CallMercenaryCoolTimeSaveData (3 fields) *(endgame only)*
  - `_characterKey`: CharacterKey [scalar, 4B]
  - `_vehicleKey`: VehicleKey [scalar, 2B]
  - `_coolTimeLeft`: TickCount64 [scalar, 8B]

### [17] PositionConstraintMotor (5 fields) *(endgame only)*
  - `_maxForce`: float [scalar, 4B]
  - `_tau`: float [scalar, 4B]
  - `_damping`: float [scalar, 4B]
  - `_proportinalRecoveryVelocity`: float [scalar, 4B]
  - `_constantRecoveryVelocity`: float [scalar, 4B]

### [18] QuestStateData (6 fields)
  - `_questKey`: QuestKey [scalar, 4B]
  - `_delayedFromQuestKey`: QuestKey [scalar, 4B]
  - `_delayTime`: uint64 [scalar, 8B]
  - `_branchedTime`: uint64 [scalar, 8B]
  - `_completedTime`: uint64 [scalar, 8B]
  - `_state`: QuestStateType [enum, 1B]

### [19] FactionPatrolSaveData (2 fields) *(endgame only)*
  - `_spawnPartySaveDataList`: ReflectObjectPtr [ObjListPtr, 0B]
  - `_factionPatrolSplineObjectUUID`: uint4 [scalar, 16B]

### [20] StoreSaveData (2 fields)
  - `_saveVersion`: uint32 [scalar, 4B]
  - `_storeDataList`: ReflectObject [ObjList, 0B]

### [21] StoreItemSaveData (5 fields)
  - `_importantSaveIndex`: uint32 [scalar, 4B]
  - `_buyPrice`: TStackCount [scalar, 8B]
  - `_sellPrice`: TStackCount [scalar, 8B]
  - `_tradeCount`: TStackCount [scalar, 8B]
  - `_stockHistorys`: ReflectObject [ObjList, 0B]

### [22] NPCScheduleStageSaveData (3 fields)
  - `_characterList`: ReflectObject [ObjList, 0B]
  - `_miseensceneSaveDataList`: ReflectObject [ObjList, 0B]
  - `_stageNameHash`: HashCode32 [scalar, 4B]

### [23] GameData_GimmickPointData (2 fields)
  - `_name`: staticstringA [string/bytes, 1B]
  - `_transform`: Transform [scalar, 40B]

### [24] LevelGimmickSceneObjectElementSaveData (4 fields) *(endgame only)*
  - `_levelGimmickSceneObjectInfoKey`: LevelGimmickSceneObjectInfoKey [scalar, 4B]
  - `_sceneObjectUuid`: uint4 [scalar, 16B]
  - `_fogPivotPosition`: float3 [scalar, 12B]
  - `_isDiscoverd`: bool [scalar, 1B]

### [25] FieldCharacterSaveData (6 fields) *(endgame only)*
  - `_characterKey`: CharacterKey [scalar, 4B]
  - `_actorStateFlagRaw`: uint32 [scalar, 4B]
  - `_deadPosition`: float3 [scalar, 12B]
  - `_deadRotationYaw`: float [scalar, 4B]
  - `_fieldInfoKey`: FieldInfoKey [scalar, 4B]
  - `_fieldNpcSaveDataKey`: FieldNPCSaveDataKey [scalar, 4B]

### [26] StoreStockHistorySaveData (3 fields)
  - `_refreshFieldTime`: uint64 [scalar, 8B]
  - `_buyPrice`: TStackCount [scalar, 8B]
  - `_sellPrice`: TStackCount [scalar, 8B]

### [27] NPCScheduleMissensceneSaveData (2 fields)
  - `_missensceneSpotFolderIndex`: uint32 [scalar, 4B]
  - `_patternSaveDataList`: ReflectObject [ObjList, 0B]

### [28] StageStateData (15 fields)
  - `_key`: StageKey [scalar, 4B]
  - `_state`: QuestStateType [enum, 1B]
  - `_completeType`: uint8 [scalar, 1B]
  - `_isWaitBranch`: bool [scalar, 1B]
  - `_isSkipComplete`: bool [scalar, 1B]
  - `_completedCount`: uint16 [scalar, 2B]
  - `_completedTime`: uint64 [scalar, 8B]
  - `_delayedTime`: uint64 [scalar, 8B]
  - `_branchedTime`: uint64 [scalar, 8B]
  - `_discoverPivotPosition`: float3 [scalar, 12B]
  - `_delayedFromMissionKey`: MissionKey [scalar, 4B]
  - `_delayedFromStageKey`: StageKey [scalar, 4B]
  - `_subTimelineName`: IndexedStringA [string/bytes, 1B]
  - `_characterList`: ReflectObject [ObjList, 0B]
  - `_connectCharacterList`: ReflectObject [ObjList, 0B]

### [29] MercenaryClanSaveData (9 fields)
  - `_list`: ReflectObject [ObjList, 0B]
  - `_mercenaryDataList`: ReflectObject [ObjList, 0B]
  - `_hyosiMercenarySaveList`: ReflectObject [ObjList, 0B]
  - `_callMercenaryCoolTimeSaveList`: ReflectObject [ObjList, 0B]
  - `_callMercenarySpawnDurationSaveList`: ReflectObject [ObjList, 0B]
  - `_currentFarmUpdateDay`: uint32 [scalar, 4B]
  - `_expandedFarmSlotCount`: TFarmSlotNo [scalar, 1B]
  - `_callHyosiRemainCoolTime`: TickCount64 [scalar, 8B]
  - `_lastFocusCharacterKey`: CharacterKey [scalar, 4B]

### [30] FactionSpawnStageManagerSaveData (1 fields)
  - `_stageList`: ReflectObjectPtr [ObjListPtr, 0B]

### [31] KnowledgeSaveData (5 fields)
  - `_list`: ReflectObject [ObjList, 0B]
  - `_learnableKnowledgeList`: ReflectObject [ObjList, 0B]
  - `_learnedFollowLearnKnowledge`: ReflectObject [ObjList, 0B]
  - `_skillLearnSaveDataList`: ReflectObject [ObjList, 0B]
  - `_learnDelaySaveDataList`: ReflectObject [ObjList, 0B]

### [32] ExperienceLevelSaveData (5 fields)
  - `_level`: TLevel [scalar, 4B]
  - `_exp`: TExperience [scalar, 8B]
  - `_gimmickEventDailyCountData`: ReflectObject [ReflectObj, 8B]
  - `_actionFrameEventDailyCountData`: ReflectObject [ReflectObj, 8B]
  - `_talkEventDailyCountData`: ReflectObject [ReflectObj, 8B]

### [33] ContentsMiscSaveData (11 fields)
  - `_miniGameRecords`: ReflectObject [ObjList, 0B]
  - `_miniGameBannedDatas`: ReflectObject [ObjList, 0B]
  - `_questDialogSaveDataList`: ReflectObject [ObjList, 0B]
  - `_activatedHousingRegionKey`: RegionKey [scalar, 2B]
  - `_timeWrapCoolEndTime`: uint64 [scalar, 8B]
  - `_savedTraceSelfDestinationData`: float3 [scalar, 12B]
  - `_alertHistorySaveDataList`: ReflectObject [ObjList, 0B]
  - `_executedGameAdviceInfoKeyList`: ReflectObject [ObjList, 0B]
  - `_contentsNpcScheduleSaveDataList`: ReflectObject [ObjList, 0B]
  - `_pinMarkerDataList`: ReflectObject [ObjList, 0B]
  - `_notNoticeChallengeMissionKeyList`: MissionKey [scalar_list, 4B]

### [34] NPCScheduleMissenscenePatternSaveData (3 fields)
  - `_folderIndex`: uint32 [scalar, 4B]
  - `_respawnTimeSecond`: uint64 [scalar, 8B]
  - `_isPrevSpawnedPattern`: bool [scalar, 1B]

### [35] CallMercenarySpawnDurationSaveData (4 fields) *(endgame only)*
  - `_spawnEndDurationLeft`: TickCount64 [scalar, 8B]
  - `_mercenaryNo`: MercenaryNo [scalar, 8B]
  - `_vehicleKey`: VehicleKey [scalar, 2B]
  - `_mercenaryType`: MercenaryType [enum, 1B]

### [36] InventoryItemContentsSaveData (7 fields)
  - `_lastUpdateBankTime`: uint64 [scalar, 8B]
  - `_lastChangeInvestmentPropensityTime`: uint64 [scalar, 8B]
  - `_isFoldQuestInventory`: bool [scalar, 1B]
  - `_investmentPropensity`: InvestmentPropensity [enum, 1B]
  - `_foldItemGroupList`: ItemGroupKey [scalar_list, 2B]
  - `_bankHistoryDataList`: ReflectObject [ObjList, 0B]
  - `_minusItemDataList`: ReflectObject [ObjList, 0B]

### [37] FieldSaveData (6 fields)
  - `_saveVersion`: uint32 [scalar, 4B]
  - `_fieldInfoKey`: FieldInfoKey [scalar, 4B]
  - `_fieldGimmickSaveDataList`: ReflectObject [ObjList, 0B]
  - `_fieldGimmickSaveDataList_lostFieldGimmick`: ReflectObject [ObjList, 0B]
  - `_globalGameEventDataList`: ReflectObject [ObjList, 0B]
  - `_fieldLevelModifiedSaveDataList`: ReflectObject [ObjList, 0B]

### [38] FieldGimmickSaveData_TriggerCheckTargetData (4 fields) *(endgame only)*
  - `_targetTriggerName`: IndexedStringA [string/bytes, 1B]
  - `_rawKey`: uint32 [scalar, 4B]
  - `_triggerCheckTargetType`: GimmickTriggerCheckTargetType [enum, 1B]
  - `_count`: uint8 [scalar, 1B]

### [39] FactionSpawnStageSaveData (3 fields)
  - `_factionNodeKey`: FactionNodeKey [scalar, 4B]
  - `_factionSpawnDataKey`: FactionSpawnDataKey [scalar, 4B]
  - `_factionPatrolList`: ReflectObjectPtr [ObjListPtr, 0B]

### [40] FactionPatrolCharacterSaveData (3 fields) *(endgame only)*
  - `_fieldCharacterSaveData`: ReflectObjectPtr [ReflectObjPtr, 8B]
  - `_gameDataIndex`: uint32 [scalar, 4B]
  - `_randomValue`: float [scalar, 4B]

### [41] FactionPatrolSpawnPartySaveData (2 fields) *(endgame only)*
  - `_gameDataIndex`: uint32 [scalar, 4B]
  - `_factionPatrolCharacterSaveDataList`: ReflectObjectPtr [ObjListPtr, 0B]

### [42] InventorySaveData (5 fields)
  - `_inventorylist`: ReflectObject [ObjList, 0B]
  - `_inventoryUsableElementSaveData`: ReflectObject [ObjList, 0B]
  - `_inventoryChangedItemDataList`: ReflectObject [ObjList, 0B]
  - `_inventoryHousingGimmickSaveData`: ReflectObject [ObjList, 0B]
  - `_itemSharedCoolTimeDataList`: ReflectObject [ObjList, 0B]

### [43] InventoryElementSaveData (3 fields)
  - `_inventoryKey`: InventoryKey [scalar, 2B]
  - `_varyExpandSlotCount`: TInventorySlotNo [scalar, 2B]
  - `_itemList`: ReflectObject [ObjList, 0B]

### [44] InventorySaveData_InventoryChangedItemData (2 fields) *(endgame only)*
  - `_itemKey`: ItemKey [scalar, 4B]
  - `_changedInventoryKey`: InventoryKey [scalar, 2B]

### [45] InventorySaveData_ItemSharedCoolTimeData (2 fields) *(endgame only)*
  - `_sharedGroupName`: HashCode32 [scalar, 4B]
  - `_chargedUseableCount`: TickCount64 [scalar, 8B]

### [46] KnowledgeElementSaveData (4 fields) *(endgame only)*
  - `_key`: KnowledgeKey [scalar, 4B]
  - `_level`: TLevel [scalar, 4B]
  - `_learnedFieldTime`: uint64 [scalar, 8B]
  - `_isNewMark`: bool [scalar, 1B]

### [47] RagdollConstraintData (23 fields) *(endgame only)*
  - `_pivotTransform`: Transform [scalar, 40B]
  - `_useTargetPivotTransformForEachBodySpace`: bool [scalar, 1B]
  - `_targetPivotTransform`: Transform [scalar, 40B]
  - `_overrideDummyBodyTransform`: bool [scalar, 1B]
  - `_dummyBodyTransformInWorld`: Transform [scalar, 40B]
  - `_targetSceneObject`: ReflectObjectReferenceBase2 [string/bytes, 1B]
  - `_targetMeshNodeIndex`: int [scalar, 4B]
  - `_targetSocketName`: IndexedStringA [string/bytes, 1B]
  - `_selfSocketName`: IndexedStringA [string/bytes, 1B]
  - `_breakingThreshold`: float [scalar, 4B]
  - `_disableCollisionWithTarget`: bool [scalar, 1B]
  - `_coneAngularLimit`: float [scalar, 4B]
  - `_minTwistAngularLimit`: float [scalar, 4B]
  - `_maxTwistAngularLimit`: float [scalar, 4B]
  - `_minPlaneAngularLimit`: float [scalar, 4B]
  - `_maxPlaneAngularLimit`: float [scalar, 4B]
  - `_maxFrictionTorque`: float [scalar, 4B]
  - `_angularLimitsTauFactor`: float [scalar, 4B]
  - `_angularLimitsDampFactor`: float [scalar, 4B]
  - `_useMotor`: bool [scalar, 1B]
  - `_coneMotorIndex`: int [scalar, 4B]
  - `_twistMotorIndex`: int [scalar, 4B]
  - `_planeMotorIndex`: int [scalar, 4B]

### [48] MercenarySaveData (42 fields)
  - `_characterKey`: CharacterKey [scalar, 4B]
  - `_factionKey`: FactionKey [scalar, 4B]
  - `_mercenaryNo`: MercenaryNo [scalar, 8B]
  - `_ownedCharacterKey`: CharacterKey [scalar, 4B]
  - `_mercenaryName`: staticstringA [string/bytes, 1B]
  - `_nudeAppearanceIndexKey`: CharacterAppearanceIndexKey [scalar, 8B]
  - `_customizationAppearanceIndexKey`: CharacterAppearanceIndexKey [scalar, 8B]
  - `_armorDyeAppearanceIndexKey`: uint8 [scalar, 1B]
  - `_levelData`: ReflectObject [ReflectObj, 8B]
  - `_remainSkillPoint`: TSkillPoint [scalar, 2B]
  - `_deadTime`: Ctc64 [scalar, 8B]
  - `_lastPaidTime`: uint64 [scalar, 8B]
  - `_lastBreedingTime`: uint64 [scalar, 8B]
  - `_nextFeedFromCampStrawTime`: uint64 [scalar, 8B]
  - `_workPlaceFactionNodeKey`: FactionNodeKey [scalar, 4B]
  - `_workStartTime`: uint64 [scalar, 8B]
  - `_onlyWorkStartTime`: uint64 [scalar, 8B]
  - `_onlyWorkCompleteTime`: uint64 [scalar, 8B]
  - `_workCompleteTime`: uint64 [scalar, 8B]
  - `_workKeyNameHash`: HashCode32 [scalar, 4B]
  - `_movedDistance`: float [scalar, 4B]
  - `_totalDistance`: float [scalar, 4B]
  - `_moveVelocity`: float [scalar, 4B]
  - `_lastSummoned`: bool [scalar, 1B]
  - `_spawnPosition`: float3 [scalar, 12B]
  - `_spawnYaw`: float [scalar, 4B]
  - `_spawnFieldInfoKey`: FieldInfoKey [scalar, 4B]
  - `_isMainMercenary`: bool [scalar, 1B]
  - `_isInitialize`: bool [scalar, 1B]
  - `_isDead`: bool [scalar, 1B]
  - `_isBlockedAbility`: bool [scalar, 1B]
  - `_isHyosiMercenary`: bool [scalar, 1B]
  - `_equipItemList`: ReflectObject [ObjList, 0B]
  - `_inventoryItemList`: ReflectObject [ObjList, 0B]
  - `_occupationState`: MercenaryOccupationState [enum, 1B]
  - `_customizationSaveData`: ReflectObjectPtr [ReflectObjPtr, 8B]
  - `_remainTimeBuffSaveDataList`: ReflectObject [ObjList, 0B]
  - `_recoveryItemNo`: ItemNo [scalar, 8B]
  - `_sealedDropResultSubSaveItemList`: ReflectObject [ObjList, 0B]
  - `_useItemReserveSlotSaveList`: ReflectObject [ObjList, 0B]
  - `_currentHp`: TStat [scalar, 8B]
  - `_currentMp`: TStat [scalar, 8B]

### [49] FriendlyElementSaveData (4 fields) *(endgame only)*
  - `_characterKey`: CharacterKey [scalar, 4B]
  - `_levelData`: ReflectObject [ReflectObj, 8B]
  - `_threatRewarded`: bool [scalar, 1B]
  - `_readMemoryRewarded`: bool [scalar, 1B]

### [50] FriendlyDailyCountSaveData (2 fields)
  - `_lastUpdateTime`: uint64 [scalar, 8B]
  - `_dailyCount`: uint32 [scalar, 4B]

### [51] SimpleRunLengthEncodingSaveData (3 fields)
  - `_jumpingTable`: uint32 [scalar_list, 4B]
  - `_codeList`: uint8 [scalar_list, 1B]
  - `_lengthList`: uint8 [scalar_list, 1B]

### [52] QuestSaveData (10 fields)
  - `_stageStateData`: ReflectObject [ObjList, 0B]
  - `_missionStateList`: ReflectObject [ObjList, 0B]
  - `_questStateList`: ReflectObject [ObjList, 0B]
  - `_questGaugeStateList`: ReflectObject [ObjList, 0B]
  - `_savedTraceMissionKey`: MissionKey [scalar, 4B]
  - `_lastCompletedMissionKey`: MissionKey [scalar, 4B]
  - `_loadingTargetStageKey`: StageKey [scalar, 4B]
  - `_loadingTargetSubTimeline`: IndexedStringA [string/bytes, 1B]
  - `_savedTraceSelfDestinationData`: float3 [scalar, 12B]
  - `_questSaveVersion`: uint32 [scalar, 4B]

### [53] FieldGimmickSaveData (43 fields)
  - `_fieldGimmickSaveDataKey`: FieldGimmickSaveDataKey [scalar, 4B]
  - `_fieldSaveDataReason`: FieldSaveDataReason [enum, 1B]
  - `_saveRootFieldGimmickSaveDataKey`: FieldGimmickSaveDataKey [scalar, 4B]
  - `_resetTimeSecondsOfDays`: uint64 [scalar, 8B]
  - `_ownerLevelName`: staticstringA [string/bytes, 1B]
  - `_stageKey`: StageKey [scalar, 4B]
  - `_levelOriginSceneObjectUuid`: uint4 [scalar, 16B]
  - `_item`: ReflectObject [ReflectObj, 8B]
  - `_autoSpawnOwnerData`: ReflectObject [ReflectObj, 8B]
  - `_gimmickInfoKey`: GimmickInfoKey [scalar, 4B]
  - `_npcScheduleKey`: NPCScheduleKeyNew [scalar, 8B]
  - `_transform`: Transform [scalar, 40B]
  - `_originSpawnTransform`: Transform [scalar, 40B]
  - `_initStateNameHash`: HashCode32 [scalar, 4B]
  - `_installationTime`: uint64 [scalar, 8B]
  - `_installationAdditionalTime`: uint32 [scalar, 4B]
  - `_installationGrowthLevel`: int8 [scalar, 1B]
  - `_fertilizerAmount`: uint32 [scalar, 4B]
  - `_fertilizerLastUpdateTime`: uint64 [scalar, 8B]
  - `_dialTurnRotatedAngle`: float [scalar, 4B]
  - `_spawnReason`: HashCode32 [scalar, 4B]
  - `_aliasName`: staticstringA [string/bytes, 1B]
  - `_leftDropRollCount`: uint32 [scalar, 4B]
  - `_spawnStyle`: SpawnStyle [enum, 1B]
  - `_saveByCheat`: bool [scalar, 1B]
  - `_isBroken`: bool [scalar, 1B]
  - `_isSpreadBroken`: bool [scalar, 1B]
  - `_isLockState`: bool [scalar, 1B]
  - `_isLogoutFromGimmick`: bool [scalar, 1B]
  - `_isLogoutedAwayFromOriginTransform`: bool [scalar, 1B]
  - `_isActivateAwayFromOriginTransform`: bool [scalar, 1B]
  - `_isRaiseGamePlayLevelGimmickComplete`: bool [scalar, 1B]
  - `_levelOrigin_disabledSceneObjectUuidList`: uint4 [scalar_list, 16B]
  - `_fieldGimmickSaveData_AttachToSocketList`: ReflectObject [ObjList, 0B]
  - `_fieldGimmickSaveData_AutoSpawnChildList`: ReflectObject [ObjList, 0B]
  - `_fieldGimmickSaveData_CombinationChildList`: ReflectObject [ObjList, 0B]
  - `_fieldGimmickSaveData_TriggerCheckTargetDataList`: ReflectObject [ObjList, 0B]
  - `_fieldGimmickSaveData_ConstraintList`: ReflectObject [ObjList, 0B]
  - `_fieldGimmickSaveData_SaveTriggerGimmickList`: FieldGimmickSaveDataKey [scalar_list, 4B]
  - `_fieldGimmickSaveData_TargetedConstraintList`: FieldGimmickSaveDataKey [scalar_list, 4B]
  - `_gimmickPointDataList`: ReflectObject [ObjList, 0B]
  - `_fieldGimmickSocketIndex`: uint32 [scalar_list, 4B]
  - `_gimmickVariableList`: ReflectObject [ObjList, 0B]

### [54] FieldGimmickSaveData_Constraint (7 fields) *(endgame only)*
  - `_fieldGimmickSaveDataKey`: FieldGimmickSaveDataKey [scalar, 4B]
  - `_targetFieldGimmickSaveDataKey`: FieldGimmickSaveDataKey [scalar, 4B]
  - `_constraintName`: IndexedStringA [string/bytes, 1B]
  - `_gimmickTargetType`: GimmickTargetType [enum, 1B]
  - `_isTarget`: bool [scalar, 1B]
  - `_constraintData`: ReflectObjectPtr [ReflectObjPtr, 8B]
  - `_constraintMotor`: ReflectObjectPtr [ReflectObjPtr, 8B]

### [55] StageConnectActorData (3 fields) *(endgame only)*
  - `_nodeId`: uint32 [scalar, 4B]
  - `_characterKey`: CharacterKey [scalar, 4B]
  - `_mercenaryNo`: MercenaryNo [scalar, 8B]

### [56] QuestGaugeStateData (6 fields)
  - `_key`: QuestGaugeKey [scalar, 4B]
  - `_killRatio`: float [scalar, 4B]
  - `_stageList`: ReflectObject [ObjList, 0B]
  - `_factionOperationList`: ReflectObject [ObjList, 0B]
  - `_state`: QuestStateType [enum, 1B]
  - `_deadCount_deprecated`: uint16 [scalar, 2B]

### [57] FriendlySaveData (1 fields)
  - `_friendlyDataList`: ReflectObject [ObjList, 0B]

### [58] FollowLearnElementSaveData (2 fields) *(endgame only)*
  - `_knowledgeKey`: KnowledgeKey [scalar, 4B]
  - `_learnFromTypeRaw`: uint8 [scalar, 1B]

### [59] TransformSaveData (2 fields)
  - `_lastfieldInfoKey`: FieldInfoKey [scalar, 4B]
  - `_fieldSaveDataList`: ReflectObject [ObjList, 0B]

### [60] SkillLearnElementSaveData (2 fields) *(endgame only)*
  - `_knowledgeKey`: KnowledgeKey [scalar, 4B]
  - `_usedArtifactCount`: TStackCount [scalar, 8B]

### [61] AlertHistorySaveData (42 fields)
  - `_saveVersion`: uint32 [scalar, 4B]
  - `_alertType`: AlertType [enum, 1B]
  - `_knowledgeKey`: KnowledgeKey [scalar, 4B]
  - `_level`: TLevel [scalar, 4B]
  - `_characterName`: staticstringA [string/bytes, 1B]
  - `_toLevel`: TLevel [scalar, 4B]
  - `_expandVaryCount`: uint16 [scalar, 2B]
  - `_mercenaryType`: MercenaryType [enum, 1B]
  - `_characterKey`: CharacterKey [scalar, 4B]
  - `_currValue`: TExperience [scalar, 8B]
  - `_varyValue`: TExperience [scalar, 8B]
  - `_missionKey`: MissionKey [scalar, 4B]
  - `_questGroupKey`: QuestGroupKey [scalar, 2B]
  - `_subLevelKey`: SubLevelKey [scalar, 4B]
  - `_currentExp`: int64 [scalar, 8B]
  - `_varyExp`: int64 [scalar, 8B]
  - `_itemKey`: ItemKey [scalar, 4B]
  - `_subItemKey`: ItemKey [scalar, 4B]
  - `_otherFactionInfoKey`: FactionKey [scalar, 4B]
  - `_factionRelationType`: FactionRelationType [enum, 1B]
  - `_isBlockaded`: bool [scalar, 1B]
  - `_blockadedFactionInfoKey`: FactionNodeKey [scalar, 4B]
  - `_blockadingFactionInfoKey`: FactionKey [scalar, 4B]
  - `_blockadingLineStartNodeInfoKey`: FactionNodeKey [scalar, 4B]
  - `_useBlockDay`: bool [scalar, 1B]
  - `_isBlockByPlayer`: bool [scalar, 1B]
  - `_blockEndDay`: uint32 [scalar, 4B]
  - `_blockEventKey`: uint32 [scalar, 4B]
  - `_isOperating`: bool [scalar, 1B]
  - `_alertCount`: uint32 [scalar, 4B]
  - `_operationFactionInfo`: FactionNodeKey [scalar, 4B]
  - `_titleStringInfo`: LocalStringInfoKey [scalar, 4B]
  - `_descStringInfo`: LocalStringInfoKey [scalar, 4B]
  - `_sourceFactionNode`: FactionNodeKey [scalar, 4B]
  - `_targetFactionNode`: FactionNodeKey [scalar, 4B]
  - `_researchNode`: FactionNodeKey [scalar, 4B]
  - `_researchKey`: FactionResearchKey [scalar, 4B]
  - `_stageKey`: StageKey [scalar, 4B]
  - `_craftToolKey`: CraftToolKey [scalar, 2B]
  - `_sharpnessGimmickKey`: GimmickInfoKey [scalar, 4B]
  - `_levelGimmickSceneObjectKey`: LevelGimmickSceneObjectInfoKey [scalar, 4B]
  - `_sceneObjectUuid`: uint4 [scalar, 16B]

### [62] FogSaveData (1 fields)
  - `_fogRLESaveData`: ReflectObject [ReflectObj, 8B]

### [63] LimitedHingeConstraintData (21 fields) *(endgame only)*
  - `_pivotTransform`: Transform [scalar, 40B]
  - `_useTargetPivotTransformForEachBodySpace`: bool [scalar, 1B]
  - `_targetPivotTransform`: Transform [scalar, 40B]
  - `_overrideDummyBodyTransform`: bool [scalar, 1B]
  - `_dummyBodyTransformInWorld`: Transform [scalar, 40B]
  - `_targetSceneObject`: ReflectObjectReferenceBase2 [string/bytes, 1B]
  - `_targetMeshNodeIndex`: int [scalar, 4B]
  - `_targetSocketName`: IndexedStringA [string/bytes, 1B]
  - `_selfSocketName`: IndexedStringA [string/bytes, 1B]
  - `_breakingThreshold`: float [scalar, 4B]
  - `_disableCollisionWithTarget`: bool [scalar, 1B]
  - `_minAngularLimit`: float [scalar, 4B]
  - `_maxAngularLimit`: float [scalar, 4B]
  - `_maxFrictionTorque`: float [scalar, 4B]
  - `_angularLimitsTauFactor`: float [scalar, 4B]
  - `_angularLimitsDampFactor`: float [scalar, 4B]
  - `_useMotor`: bool [scalar, 1B]
  - `_disableAngularLimitOnUsingVelocityMotor`: bool [scalar, 1B]
  - `_disableAngularLimitForced`: bool [scalar, 1B]
  - `_motorIndex`: int [scalar, 4B]
  - `_motorTargetAngle`: float [scalar, 4B]

### [64] FactionSaveData (4 fields)
  - `_lastRewardPushedDay`: uint32 [scalar, 4B]
  - `_factionElementSaveDataList`: ReflectObject [ObjList, 0B]
  - `_factionNodeElementSaveDataList`: ReflectObject [ObjList, 0B]
  - `_factionStoredOperationRewardList`: ReflectObject [ObjList, 0B]

### [65] FixedConstraintData (11 fields) *(endgame only)*
  - `_pivotTransform`: Transform [scalar, 40B]
  - `_useTargetPivotTransformForEachBodySpace`: bool [scalar, 1B]
  - `_targetPivotTransform`: Transform [scalar, 40B]
  - `_overrideDummyBodyTransform`: bool [scalar, 1B]
  - `_dummyBodyTransformInWorld`: Transform [scalar, 40B]
  - `_targetSceneObject`: ReflectObjectReferenceBase2 [string/bytes, 1B]
  - `_targetMeshNodeIndex`: int [scalar, 4B]
  - `_targetSocketName`: IndexedStringA [string/bytes, 1B]
  - `_selfSocketName`: IndexedStringA [string/bytes, 1B]
  - `_breakingThreshold`: float [scalar, 4B]
  - `_disableCollisionWithTarget`: bool [scalar, 1B]

### [66] FieldGimmickSaveData_CombinationChild (2 fields) *(endgame only)*
  - `_gimmickInfoKey`: GimmickInfoKey [scalar, 4B]
  - `_fieldGimmickSaveDataKey`: FieldGimmickSaveDataKey [scalar, 4B]

### [67] FactionNodeSubInnerEnableElementSaveData (4 fields)
  - `_subInnerNodeKey`: FactionNodeKey [scalar, 4B]
  - `_levelNameKey`: StringInfoKey [scalar, 4B]
  - `_aliasNameKey`: StringInfoKey [scalar, 4B]
  - `_isEnable`: bool [scalar, 1B]

### [68] ItemSocketSaveData (2 fields)
  - `_currentEndurance`: TEndurance [scalar, 2B]
  - `_itemKey`: ItemKey [scalar, 4B]

### [69] BlockTiltConstraintData (11 fields) *(endgame only)*
  - `_pivotTransform`: Transform [scalar, 40B]
  - `_useTargetPivotTransformForEachBodySpace`: bool [scalar, 1B]
  - `_targetPivotTransform`: Transform [scalar, 40B]
  - `_overrideDummyBodyTransform`: bool [scalar, 1B]
  - `_dummyBodyTransformInWorld`: Transform [scalar, 40B]
  - `_targetSceneObject`: ReflectObjectReferenceBase2 [string/bytes, 1B]
  - `_targetMeshNodeIndex`: int [scalar, 4B]
  - `_targetSocketName`: IndexedStringA [string/bytes, 1B]
  - `_selfSocketName`: IndexedStringA [string/bytes, 1B]
  - `_breakingThreshold`: float [scalar, 4B]
  - `_disableCollisionWithTarget`: bool [scalar, 1B]

### [70] FieldGimmickSaveData_AttachToSocket (5 fields) *(endgame only)*
  - `_fieldGimmickSaveDataKey`: FieldGimmickSaveDataKey [scalar, 4B]
  - `_gimmickAttachMethod`: GimmickAttachMethod [enum, 1B]
  - `_selfSocketNameHash`: HashCode32 [scalar, 4B]
  - `_targetSocketNameHash`: HashCode32 [scalar, 4B]
  - `_isChild`: bool [scalar, 1B]

### [71] BallSocketConstraintData (11 fields) *(endgame only)*
  - `_pivotTransform`: Transform [scalar, 40B]
  - `_useTargetPivotTransformForEachBodySpace`: bool [scalar, 1B]
  - `_targetPivotTransform`: Transform [scalar, 40B]
  - `_overrideDummyBodyTransform`: bool [scalar, 1B]
  - `_dummyBodyTransformInWorld`: Transform [scalar, 40B]
  - `_targetSceneObject`: ReflectObjectReferenceBase2 [string/bytes, 1B]
  - `_targetMeshNodeIndex`: int [scalar, 4B]
  - `_targetSocketName`: IndexedStringA [string/bytes, 1B]
  - `_selfSocketName`: IndexedStringA [string/bytes, 1B]
  - `_breakingThreshold`: float [scalar, 4B]
  - `_disableCollisionWithTarget`: bool [scalar, 1B]

### [72] FieldGimmickSaveData_GimmickVariable (2 fields) *(endgame only)*
  - `_nameHash`: HashCode32 [scalar, 4B]
  - `_value`: int32 [scalar, 4B]

### [73] GlobalGameEventSaveData (3 fields)
  - `_refreshFieldTime`: uint64 [scalar, 8B]
  - `_globalGameEventInfoKeyList`: GlobalGameEventInfoKey [scalar_list, 2B]
  - `_varyTradeItemPriceRateList`: ReflectObject [ObjList, 0B]

### [74] GlobalGameEventSaveData_TradeItemPriceRate (2 fields)
  - `_itemGroupInfoKey`: ItemGroupKey [scalar, 2B]
  - `_varyPercent`: TPercent [scalar, 8B]

### [75] FieldLevelModifiedSaveData (2 fields)
  - `_levelNameHash`: HashCode32 [scalar, 4B]
  - `_modifiedFieldTimeSecondsOfDays`: uint64 [scalar, 8B]

### [76] RoyalSupplySaveData (1 fields)
  - `_royalSupplyElementSaveDataList`: ReflectObject [ObjList, 0B]

### [77] TransformFieldSaveData (4 fields)
  - `_fieldInfoKey`: FieldInfoKey [scalar, 4B]
  - `_fieldTimeRaw`: uint64 [scalar, 8B]
  - `_position`: float3 [scalar, 12B]
  - `_rotation`: quaternion [scalar, 16B]

### [78] RoyalSupplyElementSaveData (5 fields)
  - `_royalSupplyKey`: RoyalSupplyKey [scalar, 2B]
  - `_activeQuestKey`: QuestKey [scalar, 4B]
  - `_supplyItemKey`: ItemKey [scalar, 4B]
  - `_remainSupplyCount`: TStackCount [scalar, 8B]
  - `_isOpen`: bool [scalar, 1B]

### [79] DiscoveredLevelGimmickSceneObjectSaveData (2 fields) *(endgame only)*
  - `_saveVersion`: uint32 [scalar, 4B]
  - `_discoveredLevelGimmickSceneObjectSaveDataList`: ReflectObject [ObjList, 0B]

### [80] PlayGuideSaveData (1 fields)
  - `_playGuideKeyList`: GameAdviceInfoKey [scalar_list, 4B]

### [81] GamePlayVariableSaveData (1 fields) *(endgame only)*
  - `_gamePlayVariableElementSaveData`: ReflectObject [ObjList, 0B]

### [82] GamePlayVariableElementSaveData (2 fields) *(endgame only)*
  - `_gamePlayVariableKey`: GamePlayVariableKey [scalar, 4B]
  - `_currentVariable`: bool [scalar, 1B]

### [83] FactionElementSaveData (6 fields)
  - `_ownerFactionKey`: FactionKey [scalar, 4B]
  - `_leaderCharacterKey`: CharacterKey [scalar, 4B]
  - `_parentFactionKey`: FactionKey [scalar, 4B]
  - `_relationGroupKey`: FactionRelationGroupKey [scalar, 2B]
  - `_factionRelationDataList`: ReflectObject [ObjList, 0B]
  - `_factionApplySkillList`: ReflectObject [ObjList, 0B]

### [84] FactionRelationElementSaveData (3 fields)
  - `_targetFactionKey`: FactionKey [scalar, 4B]
  - `_relationTypeRaw`: uint8 [scalar, 1B]
  - `_dueDate`: uint32 [scalar, 4B]

### [85] FactionSkillElementsSaveData (6 fields)
  - `_targetStageKey`: StageKey [scalar, 4B]
  - `_targetQuestKey`: QuestKey [scalar, 4B]
  - `_targetRegionKey`: RegionKey [scalar, 2B]
  - `_targetPosition`: float3 [scalar, 12B]
  - `_range`: float [scalar, 4B]
  - `_applySkillList`: SkillKeyAndLevel [scalar_list, 8B]

### [86] FactionNodeElementSaveData (44 fields)
  - `_ownerFactionKey`: FactionNodeKey [scalar, 4B]
  - `_factionState`: FactionNodeStateType [enum, 1B]
  - `_blockadingFactionKey`: FactionKey [scalar, 4B]
  - `_blockadingNodeKey`: FactionNodeKey [scalar, 4B]
  - `_conquerorFactionKey`: FactionKey [scalar, 4B]
  - `_researchDataKey`: FactionResearchKey [scalar, 4B]
  - `_researchProgress`: uint32 [scalar, 4B]
  - `_isResearchAlreadyStop`: bool [scalar, 1B]
  - `_isCapital`: bool [scalar, 1B]
  - `_isBlock`: bool [scalar, 1B]
  - `_isBlockByPlayer`: bool [scalar, 1B]
  - `_useBlockDay`: bool [scalar, 1B]
  - `_isSaveEnabled`: bool [scalar, 1B]
  - `_blockSubType`: FactionBlockSubType [enum, 1B]
  - `_blockEndDay`: uint32 [scalar, 4B]
  - `_blockEventKey`: uint32 [scalar, 4B]
  - `_subBlockadingFactionKeyList`: FactionKey [scalar_list, 4B]
  - `_religionRange`: float [scalar, 4B]
  - `_fireArmPosition`: float3 [scalar, 12B]
  - `_fireArmRange`: float [scalar, 4B]
  - `_fireArmType`: HashCode32 [scalar, 4B]
  - `_factionOwnedItemList`: ReflectObject [ObjList, 0B]
  - `_factionDeliveryDataList`: ReflectObject [ObjList, 0B]
  - `_lastResourceItemUpdatedFieldTimeRaw`: uint64 [scalar, 8B]
  - `_lastRevivedFieldTimeRaw`: uint64 [scalar, 8B]
  - `_nextDeliveryStartFieldTimeRaw`: uint64 [scalar, 8B]
  - `_operationKey`: FactionOperationKey [scalar, 4B]
  - `_operationStartTimeRaw`: uint64 [scalar, 8B]
  - `_operationGotoEndTimeRaw`: uint64 [scalar, 8B]
  - `_operationLastUpdateTime`: uint64 [scalar, 8B]
  - `_operationCurrentProgress`: float [scalar, 4B]
  - `_operationStateType`: FactionOperationStateType [enum, 1B]
  - `_operationRewardRateByBuff`: TPercent [scalar, 8B]
  - `_operatorWorkerCount`: uint32 [scalar, 4B]
  - `_secondOperatorWorkerCount`: uint32 [scalar, 4B]
  - `_totalCombatPower`: float [scalar, 4B]
  - `_enableNode`: bool [scalar, 1B]
  - `_operatorMercenaryList`: ReflectObject [ObjList, 0B]
  - `_reviveQuestList`: QuestKey [scalar_list, 4B]
  - `_reviveStageList`: StageKey [scalar_list, 4B]
  - `_factionNodeApplySkillList`: ReflectObject [ObjList, 0B]
  - `_factionNodePropagateDataList`: ReflectObject [ObjList, 0B]
  - `_completedSubInnerGimmickUuidList`: SceneObjectUuid [scalar_list, 16B]
  - `_subInnerEnableDataList`: ReflectObject [ObjList, 0B]

### [87] FactionNodeSkillElementsSaveData (2 fields) *(endgame only)*
  - `_targetFactionKey`: FactionKey [scalar, 4B]
  - `_applySkillList`: SkillKeyAndLevel [scalar_list, 8B]

## 4. TOC Block Map

### Endgame Block Order

| # | Block Type | Count | Total Size | Notes |
|---|-----------|-------|-----------|-------|
| 0 | CharacterStatusSaveData | 1 | 35 | First at 0xB4EB |
| 1 | CustomizationSaveData | 1 | 287 | First at 0xB50E |
| 2 | SubLevelSaveData | 1 | 598 | First at 0xB62D |
| 3 | EquipmentSaveData | 1 | 824 | First at 0xB883 |
| 4 | GameEventSaveData | 1 | 8 | First at 0xBBBB |
| 5 | NPCScheduleStageManagerSaveData | 1 | 359,116 | First at 0xBBC3 |
| 6 | FactionSpawnStageManagerSaveData | 1 | 40,809 | First at 0x6368F |
| 7 | InventoryItemContentsSaveData | 1 | 25 | First at 0x6D5F8 |
| 8 | InventorySaveData | 1 | 1,289 | First at 0x6D611 |
| 9 | StoreSaveData | 1 | 584,109 | First at 0x6DB1A |
| 10 | MercenaryClanSaveData | 1 | 3,097 | First at 0xFC4C7 |
| 11 | QuestSaveData | 1 | 1,842,710 | First at 0xFD0E0 |
| 12 | FriendlySaveData | 1 | 4,236 | First at 0x2BEEF6 |
| 13 | KnowledgeSaveData | 1 | 62,343 | First at 0x2BFF82 |
| 14 | ContentsMiscSaveData | 1 | 3,131 | First at 0x2CF309 |
| 15 | FogSaveData | 1 | 26,354 | First at 0x2CFF44 |
| 16 | GameData_GimmickPointData | 841 | 55,400 | First at 0x2D6636 |
| 857 | FieldSaveData | 2 | 1,087,805 | First at 0x2E3E9E |
| 859 | RoyalSupplySaveData | 1 | 185 | First at 0x3ED7DB |
| 860 | DiscoveredLevelGimmickSceneObjectSaveData | 1 | 3,296 | First at 0x3ED894 |
| 861 | PlayGuideSaveData | 1 | 436 | First at 0x3EE574 |
| 862 | GamePlayVariableSaveData | 1 | 211 | First at 0x3EE728 |
| 863 | FieldNPCSaveData | 34 | 5,077 | First at 0x3EE7FB |
| 897 | FactionSaveData | 1 | 83,277 | First at 0x3EFBD0 |
| 898 | TransformSaveData | 1 | 95 | First at 0x40411D |

## 5. Key Block Details

### CharacterStatusSaveData
- TOC index: 0
- Offset: 0xB4EB, Size: 35
- Mask: `c7` (1B)
- Early game: offset=0x4E47, size=35
- Fields:
  - `_characterKey`: fixed_suffix = `1`
  - `_factionKey`: fixed_suffix = `1000000`
  - `_level`: fixed_suffix = `1`
  - `_currentHp`: fixed_suffix = `1125`
  - `_currentMp`: fixed_suffix = `110`

### CustomizationSaveData
- TOC index: 1
- Offset: 0xB50E, Size: 287
- Mask: `07` (1B)
- Early game: NOT PRESENT
- Fields:
  - `_meshData`: dynamic_array = `count=16 bytes=16 preview=01010606ffffffffffffffffffffffff`
  - `_decorationData`: dynamic_array = `count=250 bytes=250 preview=ffffffffffffffffffffffffffffffff`
  - `_version`: fixed_suffix = `0`

### SubLevelSaveData
- TOC index: 2
- Offset: 0xB62D, Size: 598
- Mask: `01` (1B)
- Early game: offset=0x4E6A, size=9
- Fields:
  - `_list`: object_list **(14 elements)**

### EquipmentSaveData
- TOC index: 3
- Offset: 0xB883, Size: 824
- Mask: `09` (1B)
- Early game: offset=0x4E73, size=3,078
- Fields:
  - `_equipCacheSequenceNo`: fixed_prefix = `6055`
  - `_useItemSaveList`: object_list **(8 elements)**

### GameEventSaveData
- TOC index: 4
- Offset: 0xBBBB, Size: 8
- Mask: `00` (1B)
- Early game: offset=0x5A79, size=8
- Fields:

### NPCScheduleStageManagerSaveData
- TOC index: 5
- Offset: 0xBBC3, Size: 359,116
- Mask: `01` (1B)
- Early game: offset=0x5A81, size=1,895
- Fields:
  - `_stageList`: object_list **(1338 elements)**

### FactionSpawnStageManagerSaveData
- TOC index: 6
- Offset: 0x6368F, Size: 40,809
- Mask: `01` (1B)
- Early game: offset=0x61E8, size=5,030
- Fields:
  - `_stageList`: object_list **(129 elements)**

### InventoryItemContentsSaveData
- TOC index: 7
- Offset: 0x6D5F8, Size: 25
- Mask: `19` (1B)
- Early game: offset=0x758E, size=11
- Fields:
  - `_lastUpdateBankTime`: fixed_prefix = `3138081396`
  - `_investmentPropensity`: fixed_prefix = `1`
  - `_foldItemGroupList`: dynamic_array = `count=1 bytes=2 preview=0044`

### InventorySaveData
- TOC index: 8
- Offset: 0x6D611, Size: 1,289
- Mask: `15` (1B)
- Early game: offset=0x7599, size=622
- Fields:
  - `_inventorylist`: object_list **(12 elements)**
  - `_inventoryChangedItemDataList`: object_list **(25 elements)**
  - `_itemSharedCoolTimeDataList`: object_list **(2 elements)**

### StoreSaveData
- TOC index: 9
- Offset: 0x6DB1A, Size: 584,109
- Mask: `03` (1B)
- Early game: offset=0x7807, size=495,981
- Fields:
  - `_saveVersion`: fixed_prefix = `2`
  - `_storeDataList`: object_list **(254 elements)**

### MercenaryClanSaveData
- TOC index: 10
- Offset: 0xFC4C7, Size: 3,097
- Mask: `3a01` (2B)
- Early game: offset=0x80974, size=583
- Fields:
  - `_mercenaryDataList`: object_list **(12 elements)**
  - `_callMercenaryCoolTimeSaveList`: object_list **(1 elements)**
  - `_callMercenarySpawnDurationSaveList`: object_list **(1 elements)**
  - `_currentFarmUpdateDay`: fixed_suffix = `44`
  - `_lastFocusCharacterKey`: fixed_suffix = `1`

### QuestSaveData
- TOC index: 11
- Offset: 0xFD0E0, Size: 1,842,710
- Mask: `2f02` (2B)
- Early game: offset=0x80BBB, size=1,680,154
- Fields:
  - `_stageStateData`: object_list **(46505 elements)**
  - `_missionStateList`: object_list **(4128 elements)**
  - `_questStateList`: object_list **(720 elements)**
  - `_questGaugeStateList`: object_list **(319 elements)**
  - `_lastCompletedMissionKey`: fixed_suffix = `1001690`
  - `_questSaveVersion`: fixed_suffix = `1`

### FriendlySaveData
- TOC index: 12
- Offset: 0x2BEEF6, Size: 4,236
- Mask: `01` (1B)
- Early game: offset=0x21AED5, size=8
- Fields:
  - `_friendlyDataList`: object_list **(27 elements)**

### KnowledgeSaveData
- TOC index: 13
- Offset: 0x2BFF82, Size: 62,343
- Mask: `0d` (1B)
- Early game: offset=0x21AEDD, size=12
- Fields:
  - `_list`: object_list **(966 elements)**
  - `_learnedFollowLearnKnowledge`: object_list **(592 elements)**
  - `_skillLearnSaveDataList`: object_list **(64 elements)**

### ContentsMiscSaveData
- TOC index: 14
- Offset: 0x2CF309, Size: 3,131
- Mask: `d800` (2B)
- Early game: offset=0x21AEE9, size=73
- Fields:
  - `_activatedHousingRegionKey`: fixed_prefix = `257`
  - `_timeWrapCoolEndTime`: fixed_prefix = `38171533363457`
  - `_alertHistorySaveDataList`: object_list **(30 elements)**
  - `_executedGameAdviceInfoKeyList`: object_list **(51 elements)**

### FogSaveData
- TOC index: 15
- Offset: 0x2CFF44, Size: 26,354
- Mask: `01` (1B)
- Early game: offset=0x21AF32, size=4,294
- Fields:
  - `_fogRLESaveData`: object_locator = `type=SimpleRunLengthEncodingSaveData mask=07 target=0x2CFF5D`

### FieldSaveData
- TOC index: 857
- Offset: 0x2E3E9E, Size: 1,087,600
- Mask: `37` (1B)
- Early game: offset=0x21C0BF, size=454
- Fields:
  - `_saveVersion`: fixed_prefix = `6`
  - `_fieldInfoKey`: fixed_prefix = `1`
  - `_fieldGimmickSaveDataList`: object_list **(3141 elements)**
  - `_globalGameEventDataList`: object_list **(5 elements)**
  - `_fieldLevelModifiedSaveDataList`: object_list **(414 elements)**

### RoyalSupplySaveData
- TOC index: 859
- Offset: 0x3ED7DB, Size: 185
- Mask: `01` (1B)
- Early game: offset=0x21C285, size=185
- Fields:
  - `_royalSupplyElementSaveDataList`: object_list **(4 elements)**

### DiscoveredLevelGimmickSceneObjectSaveData
- TOC index: 860
- Offset: 0x3ED894, Size: 3,296
- Mask: `03` (1B)
- Early game: NOT PRESENT
- Fields:
  - `_saveVersion`: fixed_prefix = `1`
  - `_discoveredLevelGimmickSceneObjectSaveDataList`: object_list **(59 elements)**

### PlayGuideSaveData
- TOC index: 861
- Offset: 0x3EE574, Size: 436
- Mask: `01` (1B)
- Early game: offset=0x21C33E, size=16
- Fields:
  - `_playGuideKeyList`: dynamic_array = `count=106 bytes=424 preview=b099fd9cf317c5c6887e3f6c36f6111a`

### FactionSaveData
- TOC index: 897
- Offset: 0x3EFBD0, Size: 83,277
- Mask: `06` (1B)
- Early game: offset=0x21C34E, size=77,165
- Fields:
  - `_factionElementSaveDataList`: object_list **(135 elements)**
  - `_factionNodeElementSaveDataList`: object_list **(0 elements)**

### TransformSaveData
- TOC index: 898
- Offset: 0x40411D, Size: 95
- Mask: `03` (1B)
- Early game: offset=0x22F0BB, size=95
- Fields:
  - `_lastfieldInfoKey`: fixed_prefix = `1`
  - `_fieldSaveDataList`: object_list **(1 elements)**

## 6. Inventory Bag Categories

| Index | Key | Purpose | Expand (endgame) |
|-------|-----|---------|-----------------|
| 0 | 1 | Equipment | 0 |
| 1 | 2 | General Inventory | 40 |
| 2 | 3 | Quest Items | 0 |
| 3 | 4 | Unknown4 | 0 |
| 4 | 5 | Materials | 0 |
| 5 | 8 | Consumables | 0 |
| 6 | 9 | Unknown9 | 0 |
| 7 | 10 | Quest2 | 0 |
| 8 | 11 | Unknown11 | 0 |
| 9 | 12 | Unknown12 | 0 |
| 10 | 13 | Unknown13 | 0 |
| 11 | 14 | Housing | 0 |

## 7. ItemSaveData — Complete Field Map

Field layout is **DYNAMIC** — positions depend on which mask bits are set.

| Bit | Field | Type | Size | Kind |
|-----|-------|------|------|------|
| 0 | `_saveVersion` | uint32 | 4B | scalar |
| 1 | `_itemNo` | ItemNo | 8B | scalar |
| 2 | `_itemKey` | ItemKey | 4B | scalar |
| 3 | `_slotNo` | TItemSlotNo | 2B | scalar |
| 4 | `_stackCount` | TStackCount | 8B | scalar |
| 5 | `_enchantLevel` | TEnchantLevel | 2B | scalar |
| 6 | `_useableCtc` | Ctc64 | 8B | scalar |
| 7 | `_endurance` | TEndurance | 2B | scalar |
| 8 | `_sharpness` | TEndurance | 2B | scalar |
| 9 | `_batteryStat` | TStat | 8B | scalar |
| 10 | `_maxBatteryStat` | TStat | 8B | scalar |
| 11 | `_maxSocketCount` | TSocketSlotNo | 1B | scalar |
| 12 | `_validSocketCount` | TSocketSlotNo | 1B | scalar |
| 13 | `_socketSaveDataList` | ReflectObject | 0B | ObjList |
| 14 | `_itemDyeDataList` | ReflectObject | 0B | ObjList |
| 15 | `_dropResultSubSaveItemList` | ReflectObject | 0B | ObjList |
| 16 | `_transferredItemKey` | ItemKey | 4B | scalar |
| 17 | `_currentGimmickState` | HashCode32 | 4B | scalar |
| 18 | `_chargedUseableCount` | TickCount64 | 8B | scalar |
| 19 | `_timeWhenPushItem` | Ctc64 | 8B | scalar |
| 20 | `_characterConversionData` | ReflectObjectPtr | 8B | ReflectObjPtr |
| 21 | `_isNewMark` | bool | 1B | scalar |

### Known Mask Patterns

| Mask (hex) | Size | Present Fields | When Used |
|-----------|------|---------------|-----------|
| `9f280d` | 227B | 0-4,7,11,13,16,18,19 | Simple items (consumable, material) |
| `9f282d` | 228B | 0-4,7,11,13,16,18,19,21 | Game's blank item template |
| `9f280f` | 231B | 0-4,7,11,13,16,17,18,19 | Items with gimmick state |
| `9f290d` | 229B | 0-4,7,8,11,13,16,18,19 | Items with sharpness |
| `bf280d` | 229B | 0-5,7,11,13,16,18,19 | Enchanted items |
| `bf290d` | 231B | 0-5,7,8,11,13,16,18,19 | Enchanted + sharpness |
| `9f281d` | 258B | 0-4,7,11,13,16,18,19,20 | Equipment + character conversion |
| `9f283d` | 259B | 0-4,7,11,13,16,18,19,20,21 | Equipment + conversion + newMark |
| `9f282f` | 232B | 0-4,7,11,13,16,17,18,19,21 | Blank + gimmick state |

## 8. Object Serialization Format

### Block Header
```
mask_byte_count(u16) + mask_bytes(mbc) + reserved_u32(4)
Then field data follows, decoded by type definition + mask bits
```

### Inline Object Locator (meta_kind 4)
```
mask_byte_count(u16) + mask_bytes(mbc) + type_index(u16) + reserved_u8(1)
+ sentinel1(u32=FFFFFFFF) + sentinel2(u32=FFFFFFFF) + payload_offset(u32)
Total: 17 + mbc bytes
```

### Object Pointer Locator (meta_kind 5)
```
Same as mk4 but may have 0, 1, or 3 prefix bytes before the locator body
```

### Compact List Element
```
prefix_u16(2) + mask_byte(1) + type_index(u16) + reserved_u8(1)
+ sentinel_u64(8, =FFFFFFFFFFFFFFFF) + payload_offset(u32)
Total: 18 bytes, payload follows immediately
```

### Object Payload
```
reserved_u32(4) + [field data per type+mask] + trailing_size_u32(4)
trailing_size value = (position_of_trailing_size - payload_start)
```

### Object List Header (variable format)
```
Format depends on prefix byte:
  prefix=0, bytes[1:4]=000000: count at +4 (u32), header=18 bytes
  prefix=0, else:              count at +1 (u24), header=18 bytes
  prefix=1, bytes[1:4]=010100: count at +4 (u32), header=21 bytes
  prefix=1, else:              count at +1 (u16 BE), header=19 bytes
Elements follow immediately after header
```

## 9. Store/Vendor Structure

```
StoreSaveData
  _saveVersion: u32 = 2
  _storeDataList: ObjList of StoreDataSaveData (254 vendors)
    StoreDataSaveData
      _storeKey: u16 (vendor ID)
      _lastPriceRefreshFieldTime: u64
      _storeItemList: ObjList of StoreItemSaveData (NPC stock)
      _storeSoldItemDataList: ObjList of ItemSaveData (player buyback)
      _itemSoldFieldTimeRawList: scalar_list of u64 (MUST match sold count)
      _storeSoldGimmickSaveDataList: ObjList
```

**Critical**: `_storeSoldItemDataList` count MUST equal `_itemSoldFieldTimeRawList` count.
Each sold item has a parallel timestamp. Missing timestamp = crash.

## 10. Mercenary Structure

```
MercenaryClanSaveData
  _mercenaryDataList: ObjList of MercenarySaveData (12 mercenaries endgame)
    MercenarySaveData (42 fields)
      _characterKey, _factionKey, _mercenaryNo, _mercenaryName
      _equipItemList: ObjList of ItemSaveData (mercenary equipment)
      _inventoryItemList: ObjList of ItemSaveData (mercenary inventory)
      _useItemReserveSlotSaveList: ObjList
      _recoveryItemNo: ItemNo
```

## 11. Item Cross-References

An item (ItemSaveData) can exist in multiple locations:

| Location | Path | Notes |
|----------|------|-------|
| Equipment | EquipmentSaveData._list[slot]._item | Currently equipped |
| Inventory | InventorySaveData._inventorylist[bag]._itemList | In player bags |
| Vendor buyback | StoreSaveData._storeDataList[vendor]._storeSoldItemDataList | Sold to NPC |
| Mercenary equip | MercenaryClanSaveData._mercenaryDataList[merc]._equipItemList | On mercenary |
| Mercenary inv | MercenaryClanSaveData._mercenaryDataList[merc]._inventoryItemList | Merc inventory |
| World drop | FieldSaveData._fieldGimmickSaveDataList[gimmick]._item | On ground |
| Quick slot ref | EquipmentSaveData._useItemSaveList[slot]._reserveItem | Quick-use reference |

**itemNo** must be globally unique across ALL locations.
**itemKey** must exist in the game's item definition tables.
