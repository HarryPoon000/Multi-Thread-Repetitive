# multithread-repetitive
A python module using multithreading to speed up bulk and repetitive function calls, which can be imported after adding repetitive.py to your project directory
```python
import repetitive
```

## `SingleFunc` class
```python
repetitive.SingleFunc(func, num_threads = 10, verbose = True)
```
Creates a `SingleFunc` object
- `func`: desired function to be run
- `num_threads`: number of threads to be used (optional, defaults to 10)
- `verbose`: `True` or `False` - if `True`, shows a progress bar using `tqdm` when running the function


### `run_all` function
Creates `self.num_threads` number of threads and runs the 
```python
SingleFunc.run_all(args_lst, pbar_pos = 0, desc = 'progress') -> list
```
- `args_lst`: list of tuples containing the arguments
- `pbar_pos`: position of the `tqdm` progress bar; ignore if self.verbose is False (optional, defaults to 0)
- `desc`: `string`, description of the `tqdm` progress bar; ignore if self.verbose is False (optional, defaults to "progress")
  
- returns: list of return values from the provided function; the length of the list is the same as the length of the input list `args_lst`

# Example usage
```python
import time
import threading
from tqdm import tqdm
from repetitive import SingleFunc

def func1():
  tqdm.write(str(threading.get_ident()))
  time.sleep(1)
    
F = SingleFunc(func1, 5)

lst = [() for _ in range(20)]
F.run_all(lst, 0)

```
