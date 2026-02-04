# 3PF - Packet Filter

**Ever wrote some really neat functions that you'd like to hold onto for future projects?**
***3PF can help you with that!***

## ✨ Description ✨

<ins>3PF is a tool that helps you carry your code over all your projects.</ins>

You can deploy your files into 3PF as a code library, giving it a name and version number.
If needed, you can also deploy updates for your libraries, or link them with other libraries in case there are dependencies.
Then, you can easily import any of your libraries from 3PF and into a project of your choice!


## 🛠️ Usage 🛠️

After downloading 3PF, open a terminal at the root of its repository, and type in this command to install it:
```bash
make install
```
*To uninstall 3PF, simply use the `make uninstall` command instead.*


To deploy a library into 3PF, use the following command:
```bash
3pf deploy <files>
```
You will then be asked to give your library a name and version number.

*To remove a library from 3PF, you can use `3pf rm <lib>`.*


Finally, to import a library into a project, use this command:
```bash
3pf install <lib> <dest>
```


**These instructions teach only the bare minimum required to use 3PF.**

There are various other commands that each have their own purpose *(such as `list`, `reload`, `edit`, `update`, `pack`, and more)*.

If you want to know about all of them, use this command:
```bash
3pf help
```

And if you want to know more about a specific command:
```bash
3pf <command> --help
```

We hope 3PF will come in handy for you!

<sup>📝 PP project developed by [Pathie](https://github.com/Conthrast) and [Pamplemom](https://github.com/PamplemomM).</sup>
