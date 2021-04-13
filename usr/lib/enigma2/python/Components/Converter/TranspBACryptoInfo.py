#
from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
from Poll import Poll
import os
ECM_INFO = '/tmp/ecm.info'
old_ecm_mtime = None
data = None


class TranspBACryptoInfo(Poll, Converter, object):
    IRDCRYPT = 0
    SECACRYPT = 1
    NAGRACRYPT = 2
    VIACRYPT = 3
    CONAXCRYPT = 4
    BETACRYPT = 5
    CRWCRYPT = 6
    NDSCRYPT = 7
    BISSCRYPT = 8
    TANDBERGCRYPT = 9
    BULCRYPT = 10
    POWERVUCRYPT = 11
    IRDECM = 12
    SECAECM = 13
    NAGRAECM = 14
    VIAECM = 15
    CONAXECM = 16
    BETAECM = 17
    CRWECM = 18
    NDSECM = 19
    BISSECM = 20
    TANDBERGECM = 21
    BULCRYPTECM = 22
    POWERVUECM = 23

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 2000
        self.poll_enabled = True
        if type == 'IrdCrypt':
            self.type = self.IRDCRYPT
        elif type == 'SecaCrypt':
            self.type = self.SECACRYPT
        elif type == 'NagraCrypt':
            self.type = self.NAGRACRYPT
        elif type == 'ViaCrypt':
            self.type = self.VIACRYPT
        elif type == 'ConaxCrypt':
            self.type = self.CONAXCRYPT
        elif type == 'BetaCrypt':
            self.type = self.BETACRYPT
        elif type == 'CrwCrypt':
            self.type = self.CRWCRYPT
        elif type == 'NdsCrypt':
            self.type = self.NDSCRYPT
        elif type == 'BissCrypt':
            self.type = self.BISSCRYPT
        elif type == 'TandbergCrypt':
            self.type = self.TANDBERGCRYPT
        elif type == 'BulCrypt':
            self.type = self.BULCRYPT
        elif type == 'PowerVUCrypt':
            self.type = self.POWERVUCRYPT
        elif type == 'IrdEcm':
            self.type = self.IRDECM
        elif type == 'SecaEcm':
            self.type = self.SECAECM
        elif type == 'NagraEcm':
            self.type = self.NAGRAECM
        elif type == 'ViaEcm':
            self.type = self.VIAECM
        elif type == 'ConaxEcm':
            self.type = self.CONAXECM
        elif type == 'BetaEcm':
            self.type = self.BETAECM
        elif type == 'CrwEcm':
            self.type = self.CRWECM
        elif type == 'NdsEcm':
            self.type = self.NDSECM
        elif type == 'BissEcm':
            self.type = self.BISSECM
        elif type == 'TandbergEcm':
            self.type = self.TANDBERGECM
        elif type == 'BulCryptEcm':
            self.type = self.BULCRYPTECM
        elif type == 'PowerVUEcm':
            self.type = self.POWERVUECM

    @cached
    def getBoolean(self):
        service = self.source.service
        info = service and service.info()
        if not info:
            return False
        if info.getInfo(iServiceInformation.sIsCrypted) == 1:
            currentcaid = self.getCaid()
            searchcaids = info.getInfoObject(iServiceInformation.sCAIDs)
            if self.type == self.IRDCRYPT:
                caemm = self.getCrypt('06', searchcaids)
                return caemm
            if self.type == self.SECACRYPT:
                caemm = self.getCrypt('01', searchcaids)
                return caemm
            if self.type == self.NAGRACRYPT:
                caemm = self.getCrypt('18', searchcaids)
                return caemm
            if self.type == self.VIACRYPT:
                caemm = self.getCrypt('05', searchcaids)
                return caemm
            if self.type == self.CONAXCRYPT:
                caemm = self.getCrypt('0B', searchcaids)
                return caemm
            if self.type == self.BETACRYPT:
                caemm = self.getCrypt('17', searchcaids)
                return caemm
            if self.type == self.CRWCRYPT:
                caemm = self.getCrypt('0D', searchcaids)
                return caemm
            if self.type == self.NDSCRYPT:
                caemm = self.getCrypt('09', searchcaids)
                return caemm
            if self.type == self.BISSCRYPT:
                caemm = self.getCrypt('26', searchcaids)
                return caemm
            if self.type == self.TANDBERGCRYPT:
                caemm = self.getCrypt('10', searchcaids)
                return caemm
            if self.type == self.BULCRYPT:
                caemm = self.getCrypt('4A', searchcaids)
                return caemm
            if self.type == self.POWERVUCRYPT:
                caemm = self.getCrypt('0E', searchcaids)
                return caemm
            if self.type == self.IRDECM:
                if currentcaid == '06':
                    return True
            elif self.type == self.SECAECM:
                if currentcaid == '01':
                    return True
            elif self.type == self.NAGRAECM:
                if currentcaid == '18':
                    return True
            elif self.type == self.VIAECM:
                if currentcaid == '05':
                    return True
            elif self.type == self.CONAXECM:
                if currentcaid == '0B':
                    return True
            elif self.type == self.BETAECM:
                if currentcaid == '17':
                    return True
            elif self.type == self.CRWECM:
                if currentcaid == '0D':
                    return True
            elif self.type == self.NDSECM:
                if currentcaid == '09':
                    return True
            elif self.type == self.BISSECM:
                if currentcaid == '26':
                    return True
            elif self.type == self.TANDBERGECM:
                if currentcaid == '10':
                    return True
            elif self.type == self.BULCRYPTECM:
                if currentcaid == '4A':
                    return True
            elif self.type == self.POWERVUECM:
                if currentcaid == '0E':
                    return True
        else:
            self.poll_enabled = False
        return False

    boolean = property(getBoolean)

    def getCrypt(self, iscaid, caids):
        if caids and len(caids) > 0:
            for caid in caids:
                caid = self.int2hex(caid)
                if len(caid) == 3:
                    caid = '0%s' % caid
                caid = caid[:2]
                caid = caid.upper()
                if caid == iscaid:
                    return True

        return False

    def getCaid(self):
        global old_ecm_mtime
        global data
        try:
            ecm_mtime = os.stat(ECM_INFO).st_mtime
        except:
            ecm_mtime = None

        if ecm_mtime != old_ecm_mtime:
            old_ecm_mtime = ecm_mtime
            data = self.getCaidFromEcmInfo()
        return data

    def getCaidFromEcmInfo(self):
        try:
            ecm = open(ECM_INFO, 'rb').readlines()
            info = {}
            for line in ecm:
                d = line.split(':', 1)
                if len(d) > 1:
                    info[d[0].strip()] = d[1].strip()

            caid = info.get('caid', '')
        except:
            caid = ''

        if caid:
            idx = caid.index('x')
            caid = caid[idx + 1:]
            if len(caid) == 3:
                caid = '0%s' % caid
            caid = caid[:2]
            caid = caid.upper()
        return caid

    def int2hex(self, int):
        return '%x' % int

    def changed(self, what):
        Converter.changed(self, what)
