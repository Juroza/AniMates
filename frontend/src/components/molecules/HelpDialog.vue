<template>
  <v-card class="pa-6">
    <h2>Some Helpful Tips...</h2>
    <v-divider :thickness="5"></v-divider>

    <h3>[<v-icon icon="$play" class="mr-2" />Play]</h3>
    <p>
      The Play feature allows you to preview a compiled video of your animation in browser! <br/>
      This can also help you to see how the motion in your project flows while you are making it. <br/>
      This feature also allows you to download the video to your local system, <br/>
      providing a simple service for outputting your animations.
      Just make sure to set the FPS setting of the project to an appropriate value beforehand,
      and watch your hard work come to life!
    </p>
    <v-divider :thickness="3"></v-divider>

    <h3>[<v-icon icon="$export" class="mr-2" />Export]</h3>
    <p>
      The Export feature allows you to download your animation's frames to your local computer's downloads folder, as individual images! <br/>
      This can then be used to reproduce the animation with higher control over how it is compiled,
      or can be used to further manipulate the images in whichever way you see fit!
    </p>
    <v-divider :thickness="3"></v-divider>

    <b><i>An Important Note</i></b>
    <p>
      The Play and Export features will fill gaps between frames with the data for the previous frame. <br/>
      For example, a project containing canvases for frames 1, 2 and 5 will have an output of that uses 5 frames for both Play and Export.
      Frame 1, 2 and 5 in the ouptut matches the original 1st, 2nd and 5th frames, but frames 3 and 4 are not in the original,
      so they will be copies of frame 2. <br/>
      This allows you to elongate a single image across multiple frames easily in your outputs,
      making timing controls a less tedious process.
    </p>
  </v-card>
</template>
