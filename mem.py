from memory_profiler import profile
import gc


@profile
def import_genai():
  from sentence_transformers import util
  gc.collect()  #run garbage collection to try to isolate the imports effect


gc.collect()
import_genai()
gc.collect()
