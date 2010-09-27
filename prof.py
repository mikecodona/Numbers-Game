from hotshot import stats
import hotshot
import numbers

prof = hotshot.Profile("hotshot_edi_stats")
prof.runcall(numbers.main)
prof.close()

s = stats.load("hotshot_edi_stats")
s.sort_stats("time").print_stats()
