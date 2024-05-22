from tqdm import tqdm
import threading

class SingleFunc:
    # func: function to be run
    # num_threads: number of threads to be used
    # verbose: if True, shows progress bar
    def __init__(self, func, num_threads = 10, verbose = True):
        self.func = func
        self.num_threads = num_threads
        self.verbose = verbose

        
    # args_lst: list of tuples containing the arguments
    # pbar_pos: position of progress bar, ignore if self.verbose is False; refer to tqdm.tqdm() for more information
    # desc: description of progress bar
    # returns: list of return values from the provided function
    def run_all(self, args_lst, pbar_pos = 0, desc = 'progress') -> list:
        if self.verbose:
            return self.__run_all_verbose(args_lst, pbar_pos, desc = 'progress')
        else:
            return self.__run_all_nonVerbose(args_lst)
        
    
    def __run_all_verbose(self, args_lst = None, pbar_pos = 0, desc = 'progress') -> list:
        self.indicies = list(range(len(args_lst)))
        self.threads = []
        self.__values = [0 for _ in range(len(args_lst))]

        with tqdm(total = len(args_lst), position = pbar_pos, leave = None, desc = desc) as self.pbar:
            for _ in range(self.num_threads):
                thr = threading.Thread(target = self.__manager, args = (args_lst, ))
                self.threads.append(thr)
                thr.start()

            for thr in self.threads:
                thr.join()

        return self.__values

    def __run_all_nonVerbose(self, args_lst = None) -> list:
        self.indicies = list(range(len(args_lst)))
        self.threads = []
        self.__values = [0 for _ in range(len(args_lst))]

        for _ in range(self.num_threads):
            thr = threading.Thread(target = self.__manager, args = (args_lst, ))
            self.threads.append(thr)
            thr.start()

        for thr in self.threads:
            thr.join()

        return self.__values            

    # takes the first available inputs and uses it
    def __manager(self, args_lst):
        if len(self.indicies) == 0: return
        ind = self.indicies.pop(0)
        self.__values[ind] = self.func(*(args_lst[ind]))
        if self.verbose: self.pbar.update(1)    # update progress bar
        self.__manager(args_lst)



        
if __name__ == "__main__":
    import time
    def func1():
        tqdm.write(str(threading.get_ident()))
        time.sleep(1)
        return threading.get_ident()
        
    F = SingleFunc(func1, 5)

    lst = [() for _ in range(20)]
    out = F.run_all(lst, 0)
    print(len(out)) # prints '20'
    
##    G = SingleFunc(func1, 4, False)
##    G.run_all(lst,0)
