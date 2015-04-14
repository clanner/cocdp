"""
This file contains descriptions of all ClashOfClans message formats.
See cocutils.py for a description of the format syntax.
"""
# Logic...Command::getCommandType(Logic...Command *this) { return ...; }
cmdtypes= {
        # note: low nrs are 'ServerCommand'
      1:{"name":"JoinAlliance", "format":"qsdbdd"},
      2:{"name":"LeaveAlliance", "format":"qdd"},
      3:{"name":"ChangeAvatarName", "format":"sdd"},           # name, ?, ?
      4:{"name":"DonateAllianceUnit", "format":"qddd"},
      5:{"name":"AllianceUnitReceived", "format":"sddd"},
      6:{"name":"AllianceSettingsChanged", "format":"qdd"},
      7:{"name":"DiamondsAdded", "format":"bdsdd"},
      8:{"name":"ChangeAllianceRole", "format":"qdd"},
     13:{"name":"unknowncmd_13", "format":"dddd"},

    500:{"name":"BuyBuilding", "format":"dddd"},               #  x,y,id,?
    501:{"name":"MoveBuilding", "format":"dddd"},              #  x,y,buildingid, ?
    502:{"name":"UpgradeBuilding", "format":"dbd"},            # buildingid, ?
    503:{"name":"SellBuilding", "format":"dd"},
    504:{"name":"SpeedUpConstruction", "format":"dd"},
    505:{"name":"CancelConstruction", "format":"dd"},
    506:{"name":"CollectResources", "format":"dd"},            # id,unknown   ( id>=500000000 )
    507:{"name":"ClearObstacle", "format":"dd"},               # obstacleid, ?   ( id>=503000000 )
    508:{"name":"TrainUnit", "format":"ddddd"},                # buildingid, ?, charid, ?, ?
    509:{"name":"CancelUnitProduction", "format":"dddddd"},
    510:{"name":"BuyTrap", "format":"dddd"},                   #  x,y,id,?
    511:{"name":"RequestAllianceUnits", "format":"d?(s)"},     # note: starts with LogicCommand
    512:{"name":"BuyDeco", "format":"dddd"},                   #  x,y,id,?
    513:{"name":"SpeedUpTraining", "format":"dd"},
    514:{"name":"SpeedUpClearing", "format":"dd"},
    515:{"name":"CancelUpgradeUnit", "format":"dd"},
    516:{"name":"UpgradeUnit", "format":"dddd"},
    517:{"name":"SpeedUpUpgradeUnit", "format":"dd"},
    518:{"name":"BuyResources", "format":"ddb"},               # ... : optional embedded command
    519:{"name":"MissionProgress", "format":"dd"},             # missionid, ?
    520:{"name":"UnlockBuilding", "format":"dd"},
    521:{"name":"FreeWorker", "format":"db"},                  # ... todo: optional embedded command
    522:{"name":"BuyShield", "format":"dd"},
    523:{"name":"ClaimAchievementReward", "format":"dd"},
    524:{"name":"ToggleAttackMode", "format":"dd"},
    525:{"name":"LoadTurret", "format":"dd"},
    526:{"name":"BoostBuilding", "format":"dd"},
    527:{"name":"UpgradeHero", "format":"dd"},
    528:{"name":"SpeedUpHeroUpgrade", "format":"dd"},
    529:{"name":"ToggleHeroSleep", "format":"dbd"},
    530:{"name":"SpeedUpHeroHealth", "format":"dd"},
    531:{"name":"CancelHeroUpgrade", "format":"dd"},
    532:{"name":"NewShopItemsSeen", "format":"dddd"},
    533:{"name":"MoveMultipleBuildings", "format":"#[ddd]d"},
    534:{"name":"DisbandLeague", "format":"dd"},               # ServerCommand
    535:{"name":"ChangeLeague", "format":"qddd"},              # ServerCommand
    536:{"name":"BuyFreeBuilding", "format":"ddd"},
    537:{"name":"SendAllianceMail", "format":"sd"},
    538:{"name":"LeagueNotificationsSeen", "format":"dd"},
    539:{"name":"NewsSeen", "format":"dd"},
    540:{"name":"TroopRequestMessage", "format":"sd"},
    541:{"name":"SpeedUpTroopRequest", "format":"d"},
    542:{"name":"ShareReplay", "format":"q?(s)d"},
    543:{"name":"ElderKick", "format":"q?(s)d"},
    544:{"name":"EditModeShown", "format":"d"},
    553:{"name":"unknown_553", "format":"dd"},
    560:{"name":"unknown_560", "format":"dd"},
    600:{"name":"PlaceAttacker", "format":"dddd"},             # xx,yy, charid, tick
    601:{"name":"PlaceAlliancePortal", "format":"dddd"},
    602:{"name":"EndAttackPreparation", "format":"d"},
    603:{"name":"EndCombat", "format":"d"},
    604:{"name":"CastSpell", "format":"dddd"},
    605:{"name":"PlaceHero", "format":"dddd"},
    700:{"name":"Matchmaking", "format":"ddd"},                # 0, 0, curtick
    701:{"name":"CommandFailed", "format":"ddd"},              # ServerCommand
   1000:{"name":"Debug", "format":"dd"},

    545:{"name":"Replay", "format":"#[d]d"},
    549:{"name":"UpgradeMultipleBuildings", "format":"b#[d]d"},
    546:{"name":"unknown_546", "format":"ddddd"},
    552:{"name":"unknown_552", "format":"dddb"},   # todo: verify 'b'
    548:{"name":"unknown_548", "format":"ddd"},
    568:{"name":"unknown_568", "format":"ddd"},
}

#...Message::getMessageType(...Message *this) { return ...; }
msgtypes= {
    10101:{"name":"Login", "format":"qsdddsssssdsssbsssbsd", "fields":"userid usertoken vermaj ? vermin masterhash ? openudid mac phone locale lang advuuid osver ? ? android fbaid tracking vendoruuid clientseed"},
#        print "LOGIN: v%d.%d %d %010x %08x os:%s, lang:%s, dev:%s  %s %s" % (
#                fields[2], fields[4],                # version
#                fields[3],                           # ... maybe 'stage' ?
#                fields[0],                           # userid
#                fields[13], fields[11], fields[9],   # osver, lang, phone
#                fields[2], fields[5]                 # token, masterhash
#            ) 
#        print "rest: %s open:%s mac:%s lc:%08x ad:%s %d %s adid:%s fb:%s adv:%d vend:%s seed:%08x" % (
#                fields[6],
#                fields[7],  # openid
#                fields[8],  # mac
#                fields[10], # locale
#                fields[12], # adguid
#                fields[14], #
#                fields[15],
#                fields[16], # adid
#                fields[17], # fbid
#                fields[18], # adv
#                fields[19], # venduuid
#                fields[20]) # cltseed
    10102:{"name":"LoginUsingSession"},
    10103:{"name":"CreateAccount"},
    10107:{"name":"ClientCapabilities"},
    10108:{"name":"KeepAlive", "format":""},
    10112:{"name":"AuthenticationCheck"},
    10113:{"name":"SetDeviceToken", "format":"s"},
    10116:{"name":"ResetAccount"},
    10117:{"name":"ReportUser"},
    10118:{"name":"AccountSwitched"},
    10150:{"name":"AppleBillingRequest"},
    10151:{"name":"GoogleBillingRequest"},
    10200:{"name":"CreateAvatar"},
    10201:{"name":"SelectAvatar"},
    10206:{"name":"SendChatToAvatar"},
    10212:{"name":"ChangeAvatarName", "format":"sb"},
    10501:{"name":"AcceptFriend"},
    10502:{"name":"AddFriend"},
    10503:{"name":"AskForAddableFriends"},
    10504:{"name":"AskForFriendList"},
    10506:{"name":"RemoveFriend"},
    10507:{"name":"AddFriendByEmail"},
    10509:{"name":"AddFriendByAvatarNameAndCode"},
    10512:{"name":"AskForPlayingGamecenterFriends", "format":"#[s]"},
    10513:{"name":"AskForPlayingFacebookFriends", "format":"#[s]"},
    10901:{"name":"AskForMailList"},
    10904:{"name":"TakeMailAttachments"},
    14101:{"name":"AttackResult", "format":{"..6.322":"d", "6.407..":"dd"}},             # 14101:"GoHome"
    14102:{"name":"EndClientTurn"},          # needs special decoder
    14104:{"name":"AskForTargetHomeList"},
    14106:{"name":"AttackHome"},
    14108:{"name":"ChangeHomeName"},
    14113:{"name":"VisitHome", "format":"dd"},
    14114:{"name":"HomeBattleReplay", "format":"ddd"},
    14123:{"name":"AttackMatchedHome"},
    14134:{"name":"AttackNpc", "format":"d"},        # itemid
    14201:{"name":"BindFacebookAccount", "format":"bss"},  # ?, fbid, ?
    14211:{"name":"UnbindFacebookAccount"},
    14212:{"name":"BindGamecenterAccount"},
    14262:{"name":"BindGoogleServiceAccount"},
    14301:{"name":"CreateAlliance"},
    14302:{"name":"AskForAllianceData", "format":"dd"},
    14303:{"name":"AskForJoinableAlliancesList"},
    14305:{"name":"JoinAlliance"},                    # 14305:"AskForAllianceStream",
    14306:{"name":"ChangeAllianceMemberRole"},
    14307:{"name":"KickAllianceMember"},
    14308:{"name":"LeaveAlliance"},
    14309:{"name":"AskForAllianceUnitDonations"},
    14310:{"name":"DonateAllianceUnit", "format":"ddd"},
    14315:{"name":"ChatToAllianceStream"},
    14316:{"name":"ChangeAllianceSettings"},
    14317:{"name":"RequestJoinAlliance"},
    14321:{"name":"RespondToAllianceJoinRequest"},
    14322:{"name":"SendAllianceInvitation", "format":"dd"},
    14323:{"name":"JoinAllianceUsingInvitation"},
    14324:{"name":"SearchAlliances"},
    14325:{"name":"AskForAvatarProfile", "format":"ddddb"},
    14330:{"name":"SendAllianceMail"},
    14331:{"name":"HomeShareReplay"},
    14401:{"name":"AskForAllianceRankingList", "format":{"..6.322":"?(q)", "6.407..":"?(qb)"}},
    14403:{"name":"AskForAvatarRankingList", "format":"bdd"},
    14404:{"name":"AskForAvatarLocalRankingList", "format":"bdd"},
    14405:{"name":"AskForAvatarStream"},
    14418:{"name":"RemoveAvatarStreamEntry"},
    14503:{"name":"AskForLeagueMemberList", "format":"bdd"},
    14715:{"name":"SendGlobalChatLine", "format":"s"},
    16000:{"name":"LogicDeviceLinkCodeRequest"},
    16001:{"name":"LogicDeviceLinkMenuClosed"},
    16002:{"name":"LogicDeviceLinkEnterCode", "format":"s"},
    16003:{"name":"LogicDeviceLinkConfirmYes"},
    20000:{"name":"Encryption", "format":{"..6.999":"s", "7.000..":"sd"},
            "fields":{"..6.999":"serverrandom", "7.000..":"serverrandom newscramble"}
          },
    20101:{"name":"CreateAccountResult"},  # Ok or Failed
    20103:{"name":"LoginFailed", "format":{"..6.999":"dssssssb", "7.000..":"dssssssbss"},
            "fields":"reason fingerprintjson hostname rackcdnurl itunesurl ? ? ? fingerprintjsoncomp ?"
            # note: since v7: extra ss at end
    },
    20104:{"name":"LoginOk", "format":{"..6.999":"qqsssdddsdddsssds", "7.000..":"qqsssdddsdddsssdss"},
            "fields":"userid1 userid2 usertoken facebookid gamecenterid vermaj vermin verrev devprod logincount secondsplayed ? fbappid lastplayed datejoined ? googleplusid country"},
    #  14 == "297484437009394"
    #  devprod:  'state', 'prod'
#       print "OK   uid:%s, %s, %s, %s, %s" % (fields[6], fields[10], fields[14],fields[15],fields[16])
#       print "rest: %08x,%08x==%08x,%08x  %s fb:%s v%d.%d.%d 11-13:%d,%d,%d 17,18=%d,%d" % (
#               fields[0], fields[1], fields[2], fields[3],
#               fields[4],
#               fields[5],  # fb
#               fields[7], fields[8], fields[9], # v
#               fields[11], fields[12], fields[13],
#               fields[17], fields[18])


    20105:{"name":"FriendList", "format":{"..6.999":"d#[qqsssdddd?(dddsd)]", "7.000..":"d#[qqsssdddd?(dddsdd)]"},
                                "fields":"? list [userid1 userid2 name facebookid uid ? ? ? ? clan (? ? ? name ? )]"}, # "displayformat":"%-20s %-30s : %s", "display":"[uid name clan.name]",
    20106:{"name":"FriendListUpdate"},
    20107:{"name":"AddableFriends"},
    20108:{"name":"ServerKeepAlive", "format":""},
    20109:{"name":"FriendOnlineStatus"},
    20110:{"name":"FriendLoggedIn"},
    20111:{"name":"FriendLoggedOut"},
    20117:{"name":"ReportUserStatus"},
    20118:{"name":"ChatAccountBanStatus", "format":"d"},
    20121:{"name":"BillingRequestFailed"},
    # 20133  -- server locked
    20151:{"name":"AppleBillingProcessedByServer"},
    20152:{"name":"GoogleBillingProcessedByServer"},
    20161:{"name":"ShutdownStarted"},
    20171:{"name":"PersonalBreakStarted"},
    20201:{"name":"AvatarData"},
    20202:{"name":"CreateAvatarFailed"},
    20203:{"name":"CreateAvatarOk"},
    20205:{"name":"AvatarNameChangeFailed"},
    20801:{"name":"Notification"},
    20903:{"name":"MailList"},
    24101:{"name":"OwnHomeData",
        "format":{
                  #  01234567890123      
            "6.253":   "ddqsddddqq?(qsdd)dddddssdddddddddddddd?(q)bd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]d",
            "6.322": "ddddqsddddqq?(qsdd)?(q)?(q)dddddssdddddddddddddd?(q)bdd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]d",
            "6.407":"ddddqdddbsdqq?(qsdd)?(q)?(q)dddddssdddddddddddddd?(q)bdd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]dd",
            "7.001":"ddddqdddbsdqq?(qsddd)?(q)?(q)dddddssdddddddddddddd?(q)bddd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]dd",
        },
        "fields":{
            "6.253":"? ? userid json shieldtime ? ? ? userid1 userid2 ? () ? ? ? ? ? username facebookid stars points diamonds diamonds2 ? ? trophies ? ? ? ? ? ? ? ? () ? ? resources []", #" units [] spells [] unit_upgrades [] spell_upgrades [] hero_upgrades [] hero_health [] here_state [] alliance_units [] ? [] ? [] achievements [] npcprogress [] npc_gold [] npc_elixer []",
            "6.322":"? ? timestamp ? userid json shieldtime ? ? ? userid1 userid2 ? () ? () ? () ? ? ? ? ? username facebookid stars points diamonds diamonds2 ? ? trophies ? ? ? ? ? ? ? ? () ? ? ? resources []", # " units [] spells [] unit_upgrades [] spell_upgrades [] hero_upgrades [] hero_health [] here_state [] alliance_units [] ? [] ? [] achievements [] npcprogress [] npc_gold [] npc_elixer []",
            "6.407":"? ? timestamp ? userid shieldtime ? ? ? compressed ? userid1 userid2 ? () ? () ? () ? ? ? ? ? username facebookid stars points diamonds diamonds2 ? ? trophies ? ? ? ? ? ? ? ? () ? ? ? resources []", # " units [] spells [] unit_upgrades [] spell_upgrades [] hero_upgrades [] hero_health [] here_state [] alliance_units [] ? [] ? [] achievements [] npcprogress [] npc_gold [] npc_elixer []",
            "7.001":"? ? timestamp ? userid shieldtime ? ? ? compressed ? userid1 userid2 ? () ? () ? () ? ? ? ? ? username facebookid stars points diamonds diamonds2 ? ? trophies ? ? ? ? ? ? ? ? () ? ? ? ? resources []", # " units [] spells [] unit_upgrades [] spell_upgrades [] hero_upgrades [] hero_health [] here_state [] alliance_units [] ? [] ? [] achievements [] npcprogress [] npc_gold [] npc_elixer []",
        },
    },
    24103:{"name":"AttackHomeFailed"},
    24104:{"name":"OutOfSync", "format":"ddd", "fields":"checksum ? ?"},
    24105:{"name":"TargetHomeList"},
    24106:{"name":"AttackReportList"},
    24107:{"name":"EnemyHomeData",
            "format":{
                "6.322":"dsddqsddddqq?(qsdd)?(q)?(q)dddddssdddddddddddddd?(q)bdd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]dqq?(qsdd)?(q)?(q)dddddssdddddddddddddd?(q)bdd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]db",
                "6.407":"dsddqdddbsdqq?(qsdd)?(q)?(q)dddddssdddddddddddddd?(q)bdd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]dqq?(qsdd)?(q)?(q)dddddssdddddddddddddd?(q)bdd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]db",
                "7.000..":"dsddqdddbsdqq?(qsddd)?(q)?(q)dddddssdddddddddddddd?(q)bddd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]dqq?(qsddd)?(q)?(q)dddddssdddddddddddddd?(q)bddd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]db",
            },
    },
    24109:{"name":"HomeStatusList"},
    24111:{"name":"AvailableServerCommand"},  # contains embedded command
    24112:{"name":"WaitingToGoHome", "format":"dd"},
    24113:{"name":"VisitedHomeData", "format":{
        "..6.399":"ddqsddddqq?(qsdd)?(q)?(dddd)dddssddddddddddddddbqbdd#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(ddd)#(d)#(d)#(dd)#(dd)#(dd)#(dd)?(dqq)?(qsdd)?(q)?(q)dddddssddddddddddddddbqbdd#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(ddd)#(d)#(d)#(dd)#(dd)#(dd)#(dd)",
        "6.407":"ddqdddbsdqq?(qsdd)?(q)?(dddd)dddssddddddddddddddbqbdd#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(ddd)#(d)#(d)#(dd)#(dd)#(dd)#(dd)?(dqq)?(qsdd)?(q)?(q)dddddssddddddddddddddbqbdd#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(ddd)#(d)#(d)#(dd)#(dd)#(dd)#(dd)",
        "7.001..":"ddqdddbsdqq?(qsddd)?(q)?(q)dddddssddddddddddddddbdddbdd#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(ddd)#(d)#(d)#(dd)#(dd)#(dd)#(dd)?(dqq)?(qsddd)?(q)?(q)dddddssddddddddddddddbdddbdd#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(dd)#(ddd)#(d)#(d)#(dd)#(dd)#(dd)#(dd)",
        }
    },
    24114:{"name":"HomeBattleReplayData", "format":"ss"},
    24115:{"name":"ServerError"},
    24116:{"name":"HomeBattleReplayFailed"},
    24133:{"name":"NpcData", "format":{
        "..6.999":"dsddddddbddddsdddddddddddddddbddbdd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[d]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]d",
        "7.000..":"dsddddddbddddsdddddddddddddddbddbddd#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[d]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]d",
        },
    },  #  "displayformat":"gems:%d/%d", "display":"field_17 field_18"   # [1]: json string
    24201:{"name":"FacebookAccountBound", "format":"d"},
    24202:{"name":"FacebookAccountAlreadyBound"},
    24211:{"name":"GamecenterAccountBound"},
    24212:{"name":"GamecenterAccountAlreadyBound"},
    24214:{"name":"FacebookAccountUnbound"},
    24261:{"name":"GoogleServiceAccountBound"},
    24262:{"name":"GoogleServiceAccountAlreadyBound"},
    24301:{"name":"AllianceData", "format":{
"6.322":  "qsdddddddddddsd?(q)#[qsddddddddbdbq]",
"7.000..":"qsdddddddddddsdbdd#[qsddddddddbddbq]",
"6.407":  "qsdddddddddddsd?(q)#[ddsddddddddbdbdd]",
        }},
    24302:{"name":"AllianceJoinFailed"},
    24303:{"name":"AllianceJoinOk"},
    24304:{"name":"JoinableAllianceList"},
    24305:{"name":"AllianceLeaveOk"},
    24306:{"name":"ChangeAllianceMemberRoleOk"},
    24307:{"name":"KickAllianceMemberOk"},
    24308:{"name":"AllianceMember"},
    24309:{"name":"AllianceMemberRemoved"},
    24310:{"name":"AllianceList"},
    24311:{"name":"AllianceStream", }, # see lstmtypes
    24312:{"name":"AllianceStreamEntry",
            "format":{
                "..6.999":"dddqqsdddddbdddq#[dd]bs",
                "7.000..":"dddbqqsddddddddq#[dd]bs",
            },
        },
    24318:{"name":"AllianceStreamEntryRemoved", "format":"dd"},
    24319:{"name":"AllianceJoinRequestOk"},
    24320:{"name":"AllianceJoinRequestFailed"},
    24321:{"name":"AllianceInvitationSendFailed", "format":"d"},
    24322:{"name":"AllianceInvitationSentOk", "format":""},
    24324:{"name":"unknown_24324", "format":{"..6.999":"dddb", "7.000..":"dddbqsddddddddddddd"}},     # new in v6
    24332:{"name":"AllianceCreateFailed"},
    24333:{"name":"AllianceChangeFailed"},
    24334:{"name":"AvatarProfile", "format":{
            "..6.999":"dqq?(qsdd)?(q)?(dd)dddddssdddddddqqddd?(q)?(dd)#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]sdddb",
            "7.000..":"dqq?(qsddd)?(q)?(dd)dddddssdddddddqqddd?(q)?(ddd)#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[dd]#[ddd]#[d]#[d]#[dd]#[dd]#[dd]#[dd]sdddb",
        }
    },
    24335:{"name":"unknown_24335", 
# todo: implement nested qualifiers in cocutils
#            "format":"ddqsd#[qqqsdddddddddddddddd?(q)?(q)?(dd)?(dd)ddds#[q#[dd]]]bqsd#[qqqsdddddddddddddddd?(q)?(q)?(dd)?(dd)ddds#[q#[dd]]]bddd#[ddddqqqqssdddddddbdddd]"
            },
    24338:{"name":"unknown_24338", "format":"#[qsdqsddddddbddd]", "fields":"list [clanid clanname badge1 userid username badge2]"},
    24401:{"name":"AllianceRankingList", "format":{
        "..6.400":"#[qsddddd]ddddd",
        "6.407":"#[qsddddq]ddddd",
        "7.000..":"#[qsddddqd]ddddd",
        }},
    24402:{"name":"unknown_24402", "format":{
        
        "..6.999":"#[qsdddddd]",
        "7.000..":"#[qsddddqd]",
        
        }
        },
    24403:{"name":"AvatarRankingList", "format":"#[qsdddddddddsq?(qsd)]"},
    24404:{"name":"AvatarLocalRankingList", "format":"#[qsdddddddddsq?(qsd)]"},
    24411:{"name":"AvatarStream"}, #  see vstmtypes    "format":"#[dddddsdddbsbddd?(ddd)]" 
    24412:{"name":"AvatarStreamEntry", "format":"dddddsddbdsbddd?(ddd)"}, # "displayformat":"battle result: \"%s\"", "display":"field_05"
    24418:{"name":"AvatarStreamEntryRemoved", "format":"dd"},
    24503:{"name":"LeagueMemberList", "format":"d#[qsddddddddqq?(qsd)dd]"},
    24715:{"name":"GlobalChatLine", "format":"ssdddddd?(ddsd)", "fields":"message username ? ? ? ? ? ? clan (? ? name ?)"},
    25892:{"name":"Disconnected", "format":"d"},
    26002:{"name":"LogicDeviceLinkCodeResponse", "format":"sdddd"},
    26003:{"name":"LogicDeviceLinkNewDeviceLinked"},
    26004:{"name":"LogicDeviceLinkCodeDeactivated"},
    26005:{"name":"LogicDeviceLinkResponse", "format":"sddddddd"},
    26007:{"name":"LogicDeviceLinkDone"},
    26008:{"name":"LogicDeviceLinkError"},
}

# AvatarStream types
vstmtypes= {
        2:{"name":"av2", "format":"ddddsdddbsbddd?(ddd)"},
        6:{"name":"av6", "format":"ddqsdqbsbqqsd"},
        7:{"name":"av7", "format":"ddddsdddbsbddd?(ddd)"},
}

# AllianceStream types
lstmtypes= {
1:{"name":"Donate", "format":{
"..6.999":"ddqqsddddbddd#[qddsdsdsdsds]bs", # actually: ddqqsddddbddd#[q#[ds]]bs
"7.000..":"bqqqsddddddd#[qddsdsdsdsds]bs",  # actually: bqqqsddddddd#[q#[ds]]bs
}},
2:{"name":"Chat", "format":{
    "..6.999":"ddqqsddddbs",
    "7.000..":"bqqqsdddds",
}},
#3:{"name":"JoinAllianceResponseAvatar"},
3:{"name":"JoinRequestAlliance", "format":{
    "..6.999":"ddqqsddddbssd",
    "7.000..":"bqqqsddddssd",
}},
#4:{"name":"AllianceEvent"},
4:{"name":"AllianceInvitationAvatar", "format":{
   "..6.999":"ddqqsddddbdqs",
   "7.000..":"bqqqsdddddqs",
}
},
#5:{"name":"AllianceKickOut"},
5:{"name":"Replay", "format":"ddqqsddddbdddbsssddd"},
6:{"name":"AllianceMailAvatar"},
8:{"name":"News"},
9:{"name":"DeviceLinked"},
}
#    7 incorrect masterhash
#    8 Wrong Client Version
#    9 wrong stage
#   10 Server Maintenance
#   11 Banned
#   12 Personal Break
#   13 Failed
"""
Build named constants for all commands and messages.
"""
class empty:
    pass
CMD= empty()
for k, v in cmdtypes.items():
    setattr(CMD, v["name"], k)
MSG= empty()
for k, v in msgtypes.items():
    setattr(MSG, v["name"], k)
LSTM= empty()
for k, v in lstmtypes.items():
    setattr(LSTM, v["name"], k)
VSTM= empty()
for k, v in vstmtypes.items():
    setattr(VSTM, v["name"], k)


