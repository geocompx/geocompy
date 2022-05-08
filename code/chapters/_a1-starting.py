# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Installing R and RStudio {#sec-appendix-starting}
#
# To get started with R, you need to acquire your own copy. This appendix will show you how to download R as well as RStudio, a software application that makes R easier to use. You'll go from downloading R to opening your first R session.
#
# Both R and RStudio are free and easy to download.
#
# ## How to Download and Install R
#
# R is maintained by an international team of developers who make the language available through the web page of [The Comprehensive R Archive Network](http://cran.r-project.org). The top of the web page provides three links for downloading R. Follow the link that describes your operating system: Windows, Mac, or Linux.
#
# ### Windows
#
# To install R on Windows, click the "Download R for Windows" link. Then click the "base" link. Next, click the first link at the top of the new page. This link should say something like "Download R 3.0.3 for Windows," except the 3.0.3 will be replaced by the most current version of R. The link downloads an installer program, which installs the most up-to-date version of R for Windows. Run this program and step through the installation wizard that appears. The wizard will install R into your program files folders and place a shortcut in your Start menu. Note that you'll need to have all of the appropriate administration privileges to install new software on your machine.
#
# ### Mac
#
# To install R on a Mac, click the "Download R for Mac" link. Next, click on the `R-3.0.3` package link (or the package link for the most current release of R). An installer will download to guide you through the installation process, which is very easy. The installer lets you customize your installation, but the defaults will be suitable for most users. I've never found a reason to change them. If your computer requires a password before installing new progams, you'll need it here.
#
# ::: callout-note
# ## Binaries Versus Source
#
# R can be installed from precompiled binaries or built from source on any operating system. For Windows and Mac machines, installing R from binaries is extremely easy. The binary comes preloaded in its own installer. Although you can build R from source on these platforms, the process is much more complicated and won't provide much benefit for most users. For Linux systems, the opposite is true. Precompiled binaries can be found for some systems, but it is much more common to build R from source files when installing on Linux. The download pages on [CRAN's website](http://cran.r-project.org) provide information about building R from source for the Windows, Mac, and Linux platforms.
# :::
#
# ### Linux
#
# R comes preinstalled on many Linux systems, but you'll want the newest version of R if yours is out of date. [The CRAN website](http://cran.r-project.org) provides files to build R from source on Debian, Redhat, SUSE, and Ubuntu systems under the link "Download R for Linux." Click the link and then follow the directory trail to the version of Linux you wish to install on. The exact installation procedure will vary depending on the Linux system you use. CRAN guides the process by grouping each set of source files with documentation or README files that explain how to install on your system.
#
# ::: callout-note
# ## 32-bit Versus 64-bit
#
# R comes in both 32-bit and 64-bit versions. Which should you use? In most cases, it won't matter. Both versions use 32-bit integers, which means they compute numbers to the same numerical precision. The difference occurs in the way each version manages memory. 64-bit R uses 64-bit memory pointers, and 32-bit R uses 32-bit memory pointers. This means 64-bit R has a larger memory space to use (and search through).
#
# As a rule of thumb, 32-bit builds of R are faster than 64-bit builds, though not always. On the other hand, 64-bit builds can handle larger files and data sets with fewer memory management problems. In either version, the maximum allowable vector size tops out at around 2 billion elements. If your operating system doesn't support 64-bit programs, or your RAM is less than 4 GB, 32-bit R is for you. The Windows and Mac installers will automatically install both versions if your system supports 64-bit R.
# :::
#
# ## Using R
#
# R isn't a program that you can open and start using, like Microsoft Word or Internet Explorer. Instead, R is a computer language, like C, C++, or UNIX. You use R by writing commands in the R language and asking your computer to interpret them. In the old days, people ran R code in a UNIX terminal window---as if they were hackers in a movie from the 1980s. Now almost everyone uses R with an application called RStudio, and I recommend that you do, too.
#
# ::: callout-tip
# ## R and UNIX
#
# You can still run R in a UNIX or BASH window by typing the command:
#
# ``` bash
# $ R
# ```
#
# which opens an R interpreter. You can then do your work and close the interpreter by running `q()` when you are finished.
# :::
#
# ## RStudio
#
# RStudio *is* an application like Microsoft Word---except that instead of helping you write in English, RStudio helps you write in R. I use RStudio throughout the book because it makes using R much easier. Also, the RStudio interface looks the same for Windows, Mac OS, and Linux. That will help me match the book to your personal experience.
#
# You can [download RStudio](http://www.rstudio.com/ide) for free. Just click the "Download RStudio" button and follow the simple instructions that follow. Once you've installed RStudio, you can open it like any other program on your computer---usually by clicking an icon on your desktop.
#
# ::: callout-tip
# ## The R GUIs
#
# Windows and Mac users usually do not program from a terminal window, so the Windows and Mac downloads for R come with a simple program that opens a terminal-like window for you to run R code in. This is what opens when you click the R icon on your Windows or Mac computer. These programs do a little more than the basic terminal window, but not much. You may hear people refer to them as the Windows or Mac R GUIs.
# :::
#
# When you open RStudio, a window appears with three panes in it, as in @fig-layout. The largest pane is a console window. This is where you'll run your R code and see results. The console window is exactly what you'd see if you ran R from a UNIX console or the Windows or Mac GUIs. Everything else you see is unique to RStudio. Hidden in the other panes are a text editor, a graphics window, a debugger, a file manager, and much more. You'll learn about these panes as they become useful throughout the course of this book.
#
# ![The RStudio IDE for R.](images/hopr_aa01.png){#fig-layout}
#
# ::: callout-tip
# ## Do I still need to download R?
#
# Even if you use RStudio, you'll still need to download R to your computer. RStudio helps you use the version of R that lives on your computer, but it doesn't come with a version of R on its own.
# :::
#
# ## Opening R
#
# Now that you have both R and RStudio on your computer, you can begin using R by opening the RStudio program. Open RStudio just as you would any program, by clicking on its icon or by typing "RStudio" at the Windows Run prompt.
