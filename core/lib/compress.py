import base64
import lzma
import zlib

import zstd


class Compressor(object):
    # 三种压缩工具
    TOOL_DICT = {
        'zlib': zlib,
        'lzma': lzma,
        'zstd': zstd,
    }

    def __init__(self, tool):
        self.tool = self.TOOL_DICT.get(tool)
        assert self.tool, f"param 'tool' must be in {self.TOOL_DICT.keys()}"

    def compress(self, data_str: str, is_show=False):
        """
        压缩
        Parameters
        ----------
        data_str: 待压缩数据
        is_show: 是否打印压缩比率

        Returns
        -------
        二进制数据
        """
        data_bytes = data_str.encode()
        compressed = self.tool.compress(data_bytes)
        if is_show:
            print(f"压缩前大小：{len(data_bytes) / 1024 / 1024 :.2} M")
            print(f"压缩后大小：{len(compressed) / 1024 / 1024 :.2} M")
            print(f'compress ratio =  {len(compressed) / len(data_bytes):.2}')
        return compressed

    def decompress(self, compressed_date_bytes: bytes):
        """
        解压
        Parameters
        ----------
        compressed_date_bytes: 已压缩数据,二进制数据

        Returns
        -------
        解压为字符串
        """
        return self.tool.decompress(compressed_date_bytes).decode()

    def compress_base64(self, data_str: str, is_show=False):
        """
        压缩数据，并base64转换为字符串
        """
        compressed = self.compress(data_str, is_show)
        content = base64.b64encode(compressed).decode()
        return content

    def decompress_base64(self, compressed_date_str):
        """
        将base64字符串转换为二进制，并解压数据
        """
        compressed_date_bytes = base64.b64decode(compressed_date_str.encode())
        content = self.decompress(compressed_date_bytes)
        return content


compressor = Compressor('zlib')
