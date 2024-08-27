# BookCover-DL

BookCover-DL is a wxPython app I created to make it easier to grab book covers from a couple of services (currently `lubimyczytac.pl` and `legimi.pl`). I initially considered adding an ISBN lookup feature, but it didn't get fully developed. Right now, it can only verify whether the entered ISBN is a valid or invalid number.

## Why I Made This?

The main reason I built this was to help out a blind friend who needed an easy way to get book covers. It also served as a way for me to dive into Python and the wxPython library. That said, this code is more of a playground than a polished piece of software. So, don’t take it as a guideline on how things should be done.

## What to Expect?

The code is pretty messy, to be honest. I don't plan on making any big improvements—mostly because I don't have the time or the motivation anymore. But if you find it useful, that's awesome! There isn’t much out there that does this with a simple, screen reader-friendly UI, so I hope this fills that gap for someone.

## Future Improvements

This code could really use a major rewrite and modularization. The current structure is quite messy, and a more modular approach would make it easier to maintain, extend, and understand. If you're interested in contributing, this could be a good area to focus on.

Another important aspect that could be improved is the look of the user interface (UI). Since I am blind, I designed the UI primarily for screen reader compatibility, focusing on making it accessible and functional rather than visually appealing. I can't personally verify how the UI looks, so it's possible that it could benefit from enhancements to make it more visually intuitive and attractive.

If you have experience with UI design, your contributions would be especially valuable in improving the visual aspects of the app. This could involve refining the layout, adding better styling, or making the interface more user-friendly for sighted users, while ensuring it remains accessible for those using screen readers.

## How to Develop?

If you want to tinker with the code, here's how you can get started:

1. Clone the repository:
   ```bash
   git clone https://github.com/PatrykMis/bookcover-dl.git
   ```

2. Navigate to the project directory:
   ```bash
   cd bookcover-dl
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Note: This project has been tested with Python v3.12.x and wxPython v4.2.x.

4. Run the application:
   ```bash
   python main.py
   ```

## How to Build?

If you want to create an executable, here's how to do it using pyinstaller:

1. Build the application:
   ```bash
   pyinstaller build_split.spec
   ```
   Note: It's recommended to use the multi-file output option (`build_split.spec` instead of `build_onefile.spec`) as it works better for various reasons, including better handling of dependencies and easier troubleshooting.

2. After building, make sure to keep the generated `.exe` file together with the `_internal` folder. The executable relies on files in that folder to function properly.

## How You Can Help?

Feel free to fork the repo or send a pull request if you want to clean up the code or add features. I’d appreciate any contributions, but don’t expect me to be super active in maintaining this project.

## Final Thoughts

I hope this little app is useful to someone out there. It was fun to work on, and if it helps even one person, then it was worth it.
