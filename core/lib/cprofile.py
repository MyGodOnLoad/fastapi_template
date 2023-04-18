import cProfile
import os
import pstats

BASE_PATH = './prof'


def do_cprofile():
    """
    Decorator for function profiling.
    """
    def wrapper(func):
        def profiled_func(*args, **kwargs):
            DO_PROF = os.getenv("PROFILING")
            if DO_PROF:
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                # Sort stat by internal time.
                sortby = "tottime"
                ps = pstats.Stats(profile).sort_stats(sortby)

                prof_file = func.__name__ + '.prof'
                img_file = func.__name__ + '.png'
                prof_file = os.path.join(BASE_PATH, prof_file)
                img_file = os.path.join(BASE_PATH, img_file)

                ps.dump_stats(prof_file)
                res = os.system(f"gprof2dot -f pstats {prof_file} | dot -Tpng -o {img_file}")
                if res == 0:
                    print('执行成功')
                else:
                    print('执行失败')
            else:
                result = func(*args, **kwargs)
            return result
        return profiled_func
    return wrapper
