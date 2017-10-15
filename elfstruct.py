#!/usr/bin/env python3
# Classes for ELF file serialization/deserialization
from type.enum import Enum
from type.align import align,unalign
from type.uint16 import uint16
from type.uint32 import uint32
import utils

class ELFCLASS(Enum):
    """EI_CLASS enumeration"""
    ELFCLASSNONE = 0
    ELFCLASS32 = 1
    ELFCLASS64 = 2


class ELFDATA(Enum):
    """EI_DATA enumeration"""
    ELFDATANONE = 0
    ELFDATA2LSB = 1
    ELFDATA2MSB = 2


class EV(Enum):
    """EI_VERSION enumeration"""
    EV_NONE = 0
    EV_CURRENT = 1


class ELFOSABI(Enum):
    """EI_OSABI enumeration"""
    ELFOSABI_NONE = 0
    ELFOSABI_HPUX = 1
    ELFOSABI_NETBSD = 2
    ELFOSABI_GNU = 3
    # ELFOSABI_LINUX is an alias for ELFOSABI_GNU.
    ELFOSABI_LINUX = 3
    ELFOSABI_SOLARIS = 6
    ELFOSABI_AIX = 7
    ELFOSABI_IRIX = 8
    ELFOSABI_FREEBSD = 9
    ELFOSABI_TRU64 = 10
    ELFOSABI_MODESTO = 11
    ELFOSABI_OPENBSD = 12
    ELFOSABI_OPENVMS = 13
    ELFOSABI_NSK = 14
    ELFOSABI_AROS = 15
    # A GNU extension for the ARM.
    ELFOSABI_ARM = 97
    # A GNU extension for the MSP.
    ELFOSABI_STANDALONE = 255


class Elf32_e_ident:

    def __init__(self, EI_MAG=b'\x7fELF', EI_CLASS=ELFCLASS.ELFCLASS32,
            EI_DATA=ELFDATA.ELFDATA2MSB, EI_VERSION=EV.EV_CURRENT,
            EI_OSABI=ELFOSABI.ELFOSABI_NONE, little=False):
        if isinstance(EI_MAG, bytes):
            self.EI_MAG = EI_MAG
            # TODO: check if valid and signal someone if invalid
        else:
            raise Exception('EI_MAG: wrong type: %s' % type(EI_MAG).__name__)

        if isinstance(EI_CLASS, ELFCLASS):
            self.EI_CLASS = EI_CLASS
        elif EI_CLASS in map(int, ELFCLASS):
            self.EI_CLASS = ELFCLASS(EI_CLASS)
        else:
            self.EI_CLASS = ELFCLASS[EI_CLASS]

        if isinstance(EI_DATA, ELFDATA):
            self.EI_DATA = EI_DATA
        elif EI_DATA in map(int, ELFDATA):
            self.EI_DATA = ELFDATA(EI_DATA)
        else:
            self.EI_DATA = ELFDATA[EI_DATA]

        if isinstance(EI_VERSION, EV):
            self.EI_VERSION = EI_VERSION
        elif EI_VERSION in map(int, EV):
            self.EI_VERSION = EV(EI_VERSION)
        else:
            self.EI_VERSION = EV[EI_VERSION]

        if isinstance(EI_OSABI, ELFOSABI):
            self.EI_OSABI = EI_OSABI
        elif EI_OSABI in map(int, ELFOSABI):
            self.EI_OSABI = ELFOSABI(EI_OSABI)
        else:
            self.EI_OSABI = ELFOSABI[EI_OSABI]

        self.little = little # should not be used, but for consistency set it

    def __str__(self):
        EI_MAG = self.EI_MAG
        if EI_MAG == b'\x7fELF':
            EI_MAG = "'^?ELF'"
        return '{EI_MAG=%s, EI_CLASS=%s, EI_DATA=%s, EI_VERSION=%s, '\
                'EI_OSABI=%s}' % (EI_MAG, self.EI_CLASS, self.EI_DATA,
                        self.EI_VERSION, self.EI_OSABI)

    def __repr__(self):
        return '%s(%s, %s, %s, %s, %s)' % (type(self).__name__, repr(self.EI_MAG),
                self.EI_CLASS, self.EI_DATA, self.EI_VERSION,
                self.EI_OSABI)

    def __bytes__(self):
        packet = self.EI_MAG + bytes(self.EI_CLASS) + bytes(self.EI_DATA) + \
                bytes(self.EI_VERSION) + bytes(self.EI_OSABI)
        return align(packet, 16)

    def from_bytes(b):
        saved_b = b
        EI_MAG, b = (b[:4], b[4:])
        EI_CLASS, b = ELFCLASS.from_bytes(b)
        EI_DATA, b = ELFDATA.from_bytes(b)
        EI_VERSION, b = EV.from_bytes(b)
        EI_OSABI, b = ELFOSABI.from_bytes(b)
        b = unalign(saved_b, 16)
        return Elf32_e_ident(EI_MAG=EI_MAG, EI_CLASS=EI_CLASS, EI_DATA=EI_DATA,
                EI_VERSION=EI_VERSION, EI_OSABI=EI_OSABI), b

    def __len__(self):
        return len(bytes(self))

class ET(Enum):
    """e_type enumeration"""
    ET_NONE = 0
    ET_REL = 1
    ET_EXEC = 2
    ET_DYN = 3
    ET_CORE = 4
    ET_LOOS = 0xfe00
    ET_HIOS = 0xfeff
    ET_LOPROC = 0xff00
    ET_HIPROC = 0xffff


class EM(Enum):
    """e_machine enumeration"""
    EM_NONE = 0
    EM_M32 = 1
    EM_SPARC = 2
    EM_386 = 3
    EM_68K = 4
    EM_88K = 5
    EM_IAMCU = 6
    EM_860 = 7
    EM_MIPS = 8
    EM_S370 = 9
    EM_MIPS_RS3_LE = 10
    # 11 was the old Sparc V9 ABI.
    EM_OLD_SPARC_V9 = 11
    # 12 through 14 are reserved.
    EM_PARISC = 15
    # 16 is reserved.
    # Some old PowerPC object files use 17.
    EM_PPC_OLD = 17
    EM_VPP500 = 17
    EM_SPARC32PLUS = 18
    EM_960 = 19
    EM_PPC = 20
    EM_PPC64 = 21
    EM_S390 = 22
    # 23 through 35 are served.
    EM_V800 = 36
    EM_FR20 = 37
    EM_RH32 = 38
    EM_RCE = 39
    EM_ARM = 40
    EM_ALPHA = 41
    EM_SH = 42
    EM_SPARCV9 = 43
    EM_TRICORE = 44
    EM_ARC = 45
    EM_H8_300 = 46
    EM_H8_300H = 47
    EM_H8S = 48
    EM_H8_500 = 49
    EM_IA_64 = 50
    EM_MIPS_X = 51
    EM_COLDFIRE = 52
    EM_68HC12 = 53
    EM_MMA = 54
    EM_PCP = 55
    EM_NCPU = 56
    EM_NDR1 = 57
    EM_STARCORE = 58
    EM_ME16 = 59
    EM_ST100 = 60
    EM_TINYJ = 61
    EM_X86_64 = 62
    EM_PDSP = 63
    EM_PDP10 = 64
    EM_PDP11 = 65
    EM_FX66 = 66
    EM_ST9PLUS = 67
    EM_ST7 = 68
    EM_68HC16 = 69
    EM_68HC11 = 70
    EM_68HC08 = 71
    EM_68HC05 = 72
    EM_SVX = 73
    EM_ST19 = 74
    EM_VAX = 75
    EM_CRIS = 76
    EM_JAVELIN = 77
    EM_FIREPATH = 78
    EM_ZSP = 79
    EM_MMIX = 80
    EM_HUANY = 81
    EM_PRISM = 82
    EM_AVR = 83
    EM_FR30 = 84
    EM_D10V = 85
    EM_D30V = 86
    EM_V850 = 87
    EM_M32R = 88
    EM_MN10300 = 89
    EM_MN10200 = 90
    EM_PJ = 91
    EM_OR1K = 92
    EM_ARC_A5 = 93
    EM_XTENSA = 94
    EM_VIDEOCORE = 95
    EM_TMM_GPP = 96
    EM_NS32K = 97
    EM_TPC = 98
    # Some old picoJava object files use 99 (EM_PJ is correct).
    EM_SNP1K = 99
    EM_ST200 = 100
    EM_IP2K = 101
    EM_MAX = 102
    EM_CR = 103
    EM_F2MC16 = 104
    EM_MSP430 = 105
    EM_BLACKFIN = 106
    EM_SE_C33 = 107
    EM_SEP = 108
    EM_ARCA = 109
    EM_UNICORE = 110
    EM_ALTERA_NIOS2 = 113
    EM_CRX = 114
    EM_TI_PRU = 144
    EM_AARCH64 = 183
    EM_TILEGX = 191
    # The Morph MT.
    EM_MT = 0x2530
    # DLX.
    EM_DLX = 0x5aa5
    # FRV.
    EM_FRV = 0x5441
    # Infineon Technologies 16-bit microcontroller with C166-V2 core.
    EM_X16X = 0x4688
    # Xstorym16
    EM_XSTORMY16 = 0xad45
    # Renesas M32C
    EM_M32C = 0xfeb0
    # Vitesse IQ2000
    EM_IQ2000 = 0xfeba
    # NIOS
    EM_NIOS32 = 0xfebb
    # Old AVR objects used 0x1057 (EM_AVR is correct).
    EM_AVR_OLD = 0x1057
    # Old MSP430 objects used 0x1059 (EM_MSP430 is correct).
    EM_MSP430_OLD = 0x1059
    # Old FR30 objects used 0x3330 (EM_FR30 is correct).
    EM_FR30_OLD = 0x3330
    # Old OpenRISC objects used 0x3426 and 0x8472 (EM_OR1K is correct).
    EM_OR1K_OLD = 0x3426
    # Old D10V objects used 0x7650 (EM_D10V is correct).
    EM_D10V_OLD = 0x7650
    # Old D30V objects used 0x7676 (EM_D30V is correct).
    EM_D30V_OLD = 0x7676
    # Old IP2X objects used 0x8217 (EM_IP2K is correct).
    EM_IP2K_OLD = 0x8217
    # Old PowerPC objects used 0x9025 (EM_PPC is correct).
    EM_POWERPC_OLD = 0x9025
    # Old Alpha objects used 0x9026 (EM_ALPHA is correct).
    EM_ALPHA_OLD = 0x9026
    # Old M32R objects used 0x9041 (EM_M32R is correct).
    EM_M32R_OLD = 0x9041
    # Old V850 objects used 0x9080 (EM_V850 is correct).
    EM_V850_OLD = 0x9080
    # Old S/390 objects used 0xa390 (EM_S390 is correct).
    EM_S390_OLD = 0xa390
    # Old Xtensa objects used 0xabc7 (EM_XTENSA is correct).
    EM_XTENSA_OLD = 0xabc7
    EM_MICROBLAZE_OLD = 0xbaab
    # Old MN10300 objects used 0xbeef (EM_MN10300 is correct).
    EM_MN10300_OLD = 0xbeef
    # Old MN10200 objects used 0xdead (EM_MN10200 is correct).
    EM_MN10200_OLD = 0xdead


class Elf32_Ehdr:

    def __init__(self, e_ident=None, e_type=ET.ET_REL, e_machine=EM.EM_NONE,
            e_version=1, e_entry=0, e_phoff=0, e_shoff=0, e_flags=0,
            e_ehsize=0x34, e_phentsize=0, e_phnum=0, e_shentsize=0, e_shnum=0,
            e_shstrndx=0, little=False):

        if e_ident is None:
            self.e_ident = Elf32_e_ident()
        else:
            self.e_ident = e_ident

        if isinstance(e_type, ET):
            self.e_type = e_type
        elif e_type in map(int, ET):
            self.e_type = EM(e_type)
        else:
            self.e_type = ET[e_type]

        if isinstance(e_machine, EM):
            self.e_machine = e_machine
        elif e_machine in map(int, EM):
            self.e_machine = EM(e_machine)
        else:
            self.e_machine = EM[e_machine]

        self.e_version = e_version
        self.e_entry = e_entry
        self.e_phoff = e_phoff
        self.e_shoff = e_shoff
        self.e_flags = e_flags
        self.e_ehsize = e_ehsize
        self.e_phentsize = e_phentsize
        self.e_phnum = e_phnum
        self.e_shentsize = e_shentsize
        self.e_shnum = e_shnum
        self.e_shstrndx = e_shstrndx

        self.little = little
        if self.e_ident.EI_DATA is ELFDATA.ELFDATA2LSB:
            # overriding explicit value for header consistency
            self.little = True

    def __str__(self):
        return '{e_ident=%s, e_type=%s, e_machine=%s, e_version=%s, '\
    'e_entry=%s, e_phoff=%s, e_shoff=%s, e_flags=%s, e_ehsize=%s, '\
    'e_phentsize=%s, e_phnum=%s, e_shentsize=%s, e_shnum=%s, '\
                'e_shstrndx=%s}' % (self.e_ident, self.e_type, self.e_machine,
                        self.e_version, self.e_entry, self.e_phoff,
                        self.e_shoff, self.e_flags, self.e_ehsize,
                        self.e_phentsize, self.e_phnum, self.e_shentsize,
                        self.e_shnum, self.e_shstrndx)

    def __repr__(self):
        return '%s(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' % \
    (type(self).__name__, repr(self.e_ident), self.e_type, self.e_machine,
            self.e_version, self.e_entry, self.e_phoff, self.e_shoff,
            self.e_flags, self.e_ehsize, self.e_phentsize, self.e_phnum,
            self.e_shentsize, self.e_shnum, self.e_shstrndx)

    def __bytes__(self):
        e_type = bytes(self.e_type)
        e_machine = bytes(self.e_machine)
        e_version = uint32(self.e_version)
        e_entry = uint32(self.e_entry)
        e_phoff = uint32(self.e_phoff)
        e_shoff = uint32(self.e_shoff)
        e_flags = uint32(self.e_flags)
        e_ehsize = uint16(self.e_ehsize)
        e_phentsize = uint16(self.e_phentsize)
        e_phnum = uint16(self.e_phnum)
        e_shentsize = uint16(self.e_shentsize)
        e_shnum = uint16(self.e_shnum)
        e_shstrndx = uint16(self.e_shstrndx)
        if self.little:
            e_type = bytes(reversed(e_type))
            e_machine = bytes(reversed(e_machine))
        b = bytes(self.e_ident) + bytes(e_type) + bytes(e_machine) + \
                bytes(e_version) + bytes(e_entry) + bytes(e_phoff) + \
                bytes(e_shoff) + bytes(e_flags) + bytes(e_ehsize) + \
                bytes(e_phentsize) + bytes(e_phnum) + bytes(e_shentsize) + \
                bytes(e_shnum) + bytes(e_shstrndx)
        return b

    def from_bytes(b):
        e_ident, b = Elf32_e_ident.from_bytes(b)
        # througout this function we rely only on ELF header regarding
        # endianness
        little = e_ident.EI_DATA is ELFDATA.ELFDATA2LSB
        e_type, b = ET.from_bytes(b, little=little)
        e_machine, b = EM.from_bytes(b, little=little)
        e_version, b = uint32.from_bytes(b, little=little)
        e_entry, b = uint32.from_bytes(b, little=little) # || 64b
        e_phoff, b = uint32.from_bytes(b, little=little) # || 64b
        e_shoff, b = uint32.from_bytes(b, little=little) # || 64b
        e_flags, b = uint32.from_bytes(b, little=little)
        e_ehsize, b = uint16.from_bytes(b, little=little)
        e_phentsize, b = uint16.from_bytes(b, little=little)
        e_phnum, b = uint16.from_bytes(b, little=little)
        e_shentsize, b = uint16.from_bytes(b, little=little)
        e_shnum, b = uint16.from_bytes(b, little=little)
        e_shstrndx, b = uint16.from_bytes(b, little=little)
        Ehdr = Elf32_Ehdr(e_ident=e_ident, e_type=e_type, e_machine=e_machine,
                e_version=e_version.integer, e_entry=e_entry.integer,
                e_phoff=e_phoff.integer, e_shoff=e_shoff.integer,
                e_flags=e_flags.integer, e_ehsize=e_ehsize.integer,
                e_phentsize=e_phentsize.integer, e_phnum=e_phnum.integer,
                e_shentsize=e_shentsize.integer, e_shnum=e_shnum.integer,
                e_shstrndx=e_shstrndx.integer)
        return Ehdr, b

    def __len__(self):
        return len(bytes(self))


class Elf32_Phdr:

    def __init__(self, p_type=0, p_flags=0, p_offset=0, p_vaddr=0, p_paddr=0,
            p_filesz=0, p_memsz=0, p_align=0, little=False):
        self.p_type = p_type
        self.p_flags = p_flags
        self.p_offset = p_offset
        self.p_vaddr = p_vaddr
        self.p_paddr = p_paddr
        self.p_filesz = p_filesz
        self.p_memsz = p_memsz
        self.p_align = p_align

        self.little = little

    def __str__(self):
        return '{p_type=%s, p_flags=%s, p_offset=%s, p_vaddr=%s, p_paddr=%s, '\
                'p_filesz=%s, p_memsz=%s, p_align=%s}' % (self.p_type,
                        self.p_flags, self.p_offset, self.p_vaddr, self.p_paddr,
                        self.p_filesz, self.p_memsz, self.p_align)

    def __repr__(self):
        return '%s(%s, %s, %s, %s, %s, %s, %s, %s)' % (type(self).__name__,
                self.p_type, self.p_flags, self.p_offset, self.p_vaddr,
                self.p_paddr, self.p_filesz, self.p_memsz, self.p_align)

    def __bytes__(self):
        p_type = uint32(self.p_type, little=self.little)
        p_flags = uint32(self.p_flags, little=self.little)
        p_offset = uint32(self.p_offset, little=self.little)
        p_vaddr = uint32(self.p_vaddr, little=self.little)
        p_paddr = uint32(self.p_paddr, little=self.little)
        p_filesz = uint32(self.p_filesz, little=self.little)
        p_memsz = uint32(self.p_memsz, little=self.little)
        p_align = uint32(self.p_align, little=self.little)

        return bytes(p_type) + bytes(p_flags) + bytes(p_offset) + \
                bytes(p_vaddr) + bytes(p_paddr) + bytes(p_filesz) + \
                bytes(p_memsz) + bytes(p_align)

    def from_bytes(b, little=False):
        p_type, b = uint32.from_bytes(b, little)
        p_flags, b = uint32.from_bytes(b, little)
        p_offset, b = uint32.from_bytes(b, little)
        p_vaddr, b = uint32.from_bytes(b, little)
        p_paddr, b = uint32.from_bytes(b, little)
        p_filesz, b = uint32.from_bytes(b, little)
        p_memsz, b = uint32.from_bytes(b, little)
        p_align, b = uint32.from_bytes(b, little)

        return Elf32_Phdr(p_type=p_type.integer, p_flags=p_flags.integer,
                p_offset=p_offset.integer, p_vaddr=p_vaddr.integer,
                p_paddr=p_paddr.integer, p_filesz=p_filesz.integer,
                p_memsz=p_memsz.integer, p_align=p_align.integer), b

    def __len__(self):
        return len(bytes(self))


class Elf32_Shdr:

    def __init__(self, sh_name=0, sh_type=0, sh_flags=0, sh_addr=0, sh_offset=0,
            sh_size=0, sh_link=0, sh_info=0, sh_addralign=0, sh_entsize=0,
            little=False):
        self.sh_name = sh_name
        self.sh_type = sh_type
        self.sh_flags = sh_flags
        self.sh_addr = sh_addr
        self.sh_offset = sh_offset
        self.sh_size = sh_size
        self.sh_link = sh_link
        self.sh_info = sh_info
        self.sh_addralign = sh_addralign
        self.sh_entsize = sh_entsize

        self.little = little

    def __str__(self):
        return '{sh_name=%s, sh_type=%s, sh_flags=%s, sh_addr=%s, '\
                'sh_offset=%s, sh_size=%s, sh_link=%s, sh_info=%s, '\
                'sh_addralign=%s, sh_entsize=%s}' % (self.sh_name, self.sh_type,
                        self.sh_flags, self.sh_addr, self.sh_offset,
                        self.sh_size, self.sh_link, self.sh_info,
                        self.sh_addralign, self.sh_entsize)

    def __repr__(self):
        return '%s(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' % \
    (type(self).__name__, self.sh_name, self.sh_type, self.sh_flags,
            self.sh_addr, self.sh_offset, self.sh_size, self.sh_link,
            self.sh_info, self.sh_addralign, self.sh_entsize)

    def __bytes__(self):
        sh_name = uint32(self.sh_name, little=self.little)
        sh_type = uint32(self.sh_type, little=self.little)
        sh_flags = uint32(self.sh_flags, little=self.little)
        sh_addr = uint32(self.sh_addr, little=self.little)
        sh_offset = uint32(self.sh_offset, little=self.little)
        sh_size = uint32(self.sh_size, little=self.little)
        sh_link = uint32(self.sh_link, little=self.little)
        sh_info = uint32(self.sh_info, little=self.little)
        sh_addralign = uint32(self.sh_addralign, little=self.little)
        sh_entsize = uint32(self.sh_entsize, little=self.little)

        return bytes(sh_name) + bytes(sh_type) + bytes(sh_flags) + \
                bytes(sh_addr) + bytes(sh_offset) + bytes(sh_size) + \
                bytes(sh_link) + bytes(sh_info) + bytes(sh_addralign) + \
                bytes(sh_entsize)

    def from_bytes(b, little=False):
        sh_name, b = uint32.from_bytes(b, little=little)
        sh_type, b = uint32.from_bytes(b, little=little)
        sh_flags, b = uint32.from_bytes(b, little=little)
        sh_addr, b = uint32.from_bytes(b, little=little)
        sh_offset, b = uint32.from_bytes(b, little=little)
        sh_size, b = uint32.from_bytes(b, little=little)
        sh_link, b = uint32.from_bytes(b, little=little)
        sh_info, b = uint32.from_bytes(b, little=little)
        sh_addralign, b = uint32.from_bytes(b, little=little)
        sh_entsize, b = uint32.from_bytes(b, little=little)

        return Elf32_Shdr(sh_name.integer, sh_type.integer, sh_flags.integer,
                sh_addr.integer, sh_offset.integer, sh_size.integer,
                sh_link.integer, sh_info.integer, sh_addralign.integer,
                sh_entsize.integer), b

    def __len__(self):
        return len(bytes(self))


class Elf32:
    """Complete ELF structure storage class

    Allows to craft ELF file using low-level interfaces for manipulating data
    fields and accessing headers contained inside. This class is not meant to
    provide any abstraction on top of ELF structure"""

    def __init__(self, Ehdr=None, Phdr_table=None, Shdr_table=None,
            sections=None, little=False):
        if isinstance(Ehdr, Elf32_Ehdr):
            self.Ehdr = Ehdr
        else:
            self.Ehdr = Ehdr.from_bytes(Ehdr)

        if isinstance(Phdr_table, list) and (len(Phdr_table) is 0) or (
                isinstance(Phdr_table[0], Elf32_Phdr)):
            self.Phdr_table = Phdr_table
        else:
            raise Exception('Phdr table must be a list of Elf32_Phdr objects')

        if isinstance(Shdr_table, list) and (len(Shdr_table) is 0) or (
                isinstance(Shdr_table[0], Elf32_Shdr)):
            self.Shdr_table = Shdr_table
        else:
            raise Exception('Shdr table must be a list of Elf32_Shdr objects')

        if isinstance(sections, list):
            self.sections = sections
        else:
            raise Exception('Sections must be a list containing section content')

    def __str__(self):
        return '{Ehdr=%s, Phdr_table=%s, Shdr_table=%s, sections=%s}' % \
                (self.Ehdr, self.Phdr_table, self.Shdr_table, self.sections)

    def __repr__(self):
        return '%s(%s, %s, %s, %s)' % (type(self).__name__, self.Ehdr,
                self.Phdr_table, self.Shdr_table, self.sections)

    def __bytes__(self):
        headers = {}
        headers[0] = bytes(self.Ehdr)

        # Phdrs
        cursor = self.Ehdr.e_phoff
        for Phdr in self.Phdr_table:
            headers[cursor] = Phdr
            cursor += self.Ehdr.e_phentsize

        # Shdrs
        cursor = self.Ehdr.e_shoff
        for Shdr in self.Shdr_table:
            headers[cursor] = Shdr
            cursor += self.Ehdr.e_shentsize

        # sections
        for i, Shdr in enumerate(self.Shdr_table):
            if len(self.sections[i]) != 0:
                headers[Shdr.sh_offset] = self.sections[i]

        # find file size
        end_of_file = sorted(headers.keys())[-1]
        end_of_file += len(headers[end_of_file])

        # create and populate buffer
        b = bytes(end_of_file)
        for off in headers:
            hdr = headers[off]
            size = len(hdr)

            # expand to file size
            aligned = align(bytes(off) + bytes(hdr), end_of_file)

            # xor into b
            b = utils.bytes_xor(b, aligned)
        return b

    def from_bytes(b, little=False):
        blob = b
        Ehdr, b = Elf32_Ehdr.from_bytes(b)

        # Program headers
        Phdr_a = []
        for i in range(Ehdr.e_phnum):
            Phdr, b = Elf32_Phdr.from_bytes(b)
            Phdr_a.append(Phdr)

        # Section headers
        Shdr_a = []
        b = blob[Ehdr.e_shoff:]
        for i in range(Ehdr.e_shnum):
            Shdr, b = Elf32_Shdr.from_bytes(b)
            Shdr_a.append(Shdr)

        # Sections
        sections = []
        for i, Shdr in enumerate(Shdr_a):
            first = Shdr.sh_offset
            last = first + Shdr.sh_size
            section = blob[first:last]
            sections.append(section)

        return Elf32(Ehdr, Phdr_a, Shdr_a, sections), None

    def __len__(self):
        return len(bytes(self))


if __name__ == '__main__':
    print('tests')
    print('obj->file')
    e_ident = Elf32_e_ident(EI_OSABI=ELFOSABI.ELFOSABI_GNU)
    Ehdr = Elf32_Ehdr(e_ident=e_ident, e_machine=0xbaab)
    print(Ehdr)
    import os
    fd = os.open('out.elf', os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.write(fd, bytes(Ehdr))
    os.close(fd)
    print('file->obj')
    for file in ['microblaze_0.elf', 'rot13.elf']:
        print(file)
        fd = os.open(file, os.O_RDONLY)
        b = os.read(fd, 0xffff)
        os.close(fd)
        print(len(b))
        Ehdr, b = Elf32_Ehdr.from_bytes(b)
        print(Ehdr)
        print(b[:32])

    print('full parse microblaze_0.elf')
    fd = os.open('microblaze_0.elf', os.O_RDONLY)
    blob = os.read(fd, 0xffff)
    b = blob
    os.close(fd)

    # Ehdr
    Ehdr, b = Elf32_Ehdr.from_bytes(b)
    print(Ehdr)

    # Phdr
    Phdr_a = []
    for i in range(Ehdr.e_phnum):
        Phdr, b = Elf32_Phdr.from_bytes(b)
        Phdr_a.append(Phdr)
    print(' Phdr table:')
    for i, Phdr in enumerate(Phdr_a):
        print('Phdr #%d: %s' % (i, Phdr))

    # Shdr
    Shdr_a = []
    b = blob[Ehdr.e_shoff:]
    for i in range(Ehdr.e_shnum):
        Shdr, b = Elf32_Shdr.from_bytes(b)
        Shdr_a.append(Shdr)

    # .shstr
    Shdr_shstr = Shdr_a[Ehdr.e_shstrndx]
    shstr_start = Shdr_shstr.sh_offset
    shstr_end = shstr_start + Shdr_shstr.sh_size
    print(Shdr_shstr)
    shstr = blob[shstr_start:shstr_end]

    print(' Shdr table:')
    for i, Shdr in enumerate(Shdr_a):
        Shdr_name = shstr[Shdr.sh_name:]
        Shdr_name = Shdr_name[:Shdr_name.index(b'\x00')].decode('utf-8')
        print('Shdr #%d (%s): %s' % (i, Shdr_name, Shdr))

    print('Rewrite existing ELF from one file to another')
    fd = os.open('microblaze_0.elf', os.O_RDONLY)
    b = os.read(fd, 0xffff)
    os.close(fd)
    Elf,b=Elf32.from_bytes(b)
    print(Elf)
    fd=os.open('test.elf', os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.write(fd, bytes(Elf))
    os.close(fd)

    print('test')
    fd = os.open('microblaze_0.elf', os.O_RDONLY)
    src = os.read(fd, 0xffff)
    os.close(fd)
    fd = os.open('test.elf', os.O_RDONLY)
    dst = os.read(fd, 0xffff)
    os.close(fd)
    if src == dst:
        print('OK')
    else:
        print('FAIL')
