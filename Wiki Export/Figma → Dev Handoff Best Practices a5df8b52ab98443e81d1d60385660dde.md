# Figma → Dev Handoff: Best Practices

Author: Generate Management
Branch: Software
Hidden: No
Parent page: Breaking Silos (Breaking%20Silos%202d26a01f9689444bbb069f20491b80ac.md)

**Whether you are a PL looking to scope out Figma dev for your team or a software developer looking for resources, this is the place to be!** 

### TLDR;

- **Really great info about Figma developer handoff:** [https://www.figma.com/best-practices/guide-to-developer-handoff/](https://www.figma.com/best-practices/guide-to-developer-handoff/)
- **Feel free to browse this example file to see Figma's "can view" capabilities:** [https://www.figma.com/file/ewVdWlAd3ZZ3lZSWBaTWZn/Generate:-Dev-Handoff-Example?node-id=0%3A1](https://www.figma.com/file/ewVdWlAd3ZZ3lZSWBaTWZn/Generate:-Dev-Handoff-Example?node-id=0%3A1)

### Step-by-step Guide:

- **Steps for Design Handoff:**
    1. Make sure the front-end devs on your team have Figma access. If they do not, collect their emails and either:
        1. Give them "can view" access on Figma
        2. Send the emails to the Chief Designer who will deal with permissions
    2. Once the lofis for a feature are complete, move those screens (and any accompanying prototyping) to a new page titled: "✅ Feature Name: lofis"
        1. ShowNxt example: "✅ Coach Signup: lofis"
        2. **This consistent naming convention is important** so your devs know where to look for designs!
    3. Use the [Auto Flow Plug-in](https://www.figma.com/community/plugin/733902567457592893/Autoflow) to draw connections between screens so your devs will understand the flows better
    4. 🎉 Let your team know what lofis are ready to dev! 🎉
- **Steps for Front-End Development:**
    1. Once designers let you know a feature is ready for development, open the Figma file (either within the desktop app or in a browser)
        1. If the design is ready for development, the designs will be found on the page named: "✅ Feature Name: lofis" or "✅ Feature Name: hifis"
        2. The ✅ means the designers are done making adjustments to these screens
    2. Navigate to the page you will be developing (using the left side panel) 
        
        ![Left-side pages panel_.png](Figma%20%E2%86%92%20Dev%20Handoff%20Best%20Practices%20a5df8b52ab98443e81d1d60385660dde/Left-side_pages_panel_.png)
        
    3. **BEST PART:** Select the frame (*A.K.A. art board*) you are working on, and using the **code panel** (on the right-side of the screen) you have the opportunity to view code for CSS, iOS (Swift), and Android (XML) and any descriptions added to components.
        1. You also have the ability to export any assets from the file using the **Export** feature
        2. **THIS CODE IS NOT MEANT TO BE DIRECTLY COPY & PASTED, IT SHOULD BE USED AS A HELPFUL RESOURCE**
    
    **Video for overview:** 
    
    [https://youtu.be/B242nuM3y2s](https://youtu.be/B242nuM3y2s)
    

### Components:

**Component usage is very important for both efficient design and development practices. Designers should be using components to build out their designs.** (A.K.A. symbols in sketch)
****

> **Definition: "***Components are elements you can reuse across your designs. They help to create and manage consistent designs across projects. You can create components from any layers or objects you've designed. These could be a whole range of things like buttons, icons, layouts, and more.*"
> 
> 
> — [https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-Components-in-Figma#:~:text=Components are elements you can,icons%2C layouts%2C and more](https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-Components-in-Figma#:~:text=Components%20are%20elements%20you%20can,icons%2C%20layouts%2C%20and%20more).
> 

<aside>
💡 **In other words:** Components are like puzzle pieces. A designer creates components, and reuses them as pieces of the design. If used correctly, developers should be able to create and style the components, and reuse them throughout the development process.

</aside>

**Useful Video:**

[https://youtu.be/k74IrUNaJVk?list=PLXDU_eVOJTx5LSjOmeBYMuvaa4UayfMe4](https://youtu.be/k74IrUNaJVk?list=PLXDU_eVOJTx5LSjOmeBYMuvaa4UayfMe4)

### ‼️🎨  Designers  🎨‼️

- If you haven't implemented components yet, it's okay! But it is important for you to transition your designs to be component-based.
- If you are unsure of how to do this, here are some great resources to use to learn about all things component-based design!
    - [Figma.com's resources](https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-Components-in-Figma)
    - [Figma defines component best practices](https://www.figma.com/best-practices/components-styles-and-shared-libraries/)
    - [Introduction to component variants](https://www.youtube.com/watch?v=y29Xwt9dET0)
    - [Auto Layout intro video](https://www.youtube.com/watch?v=TyaGpGDFczw)
- There are so many capabilities built into components!!!! I encourage you to learn more about using [auto layout](https://www.youtube.com/watch?v=TyaGpGDFczw), creating variants, and swapping out components easily. If you struggle with something in Figma, chances are someone has also struggled with the same thing. The internet and [figma.com](http://figma.com) have some really awesome resources to help make your design process more efficient! **(P.S. reach out to your Chief Designer with any questions, they would love to help!)**