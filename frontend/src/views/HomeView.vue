<template>
  <main>
    <MusicPlayer />
    <MusicList />
  </main>
</template>

<script>
import MusicList from '@/components/MusicList.vue';
import MusicPlayer from '@/components/MusicPlayer.vue';
export default {
  name: 'Home',
  components:{
    MusicList,
    MusicPlayer,
  },
}
</script>

