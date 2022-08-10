<script>
export default{
    data(){
        return {
            my:{
                name:"S.M.Hemant",
                lastlogtime:13
            }
        }
    }
}
</script>

<template>
    <p class="w">My first vue application {{ my }}</p>
</template>

<style>
.w{
    color:red;
    font-weight: bold;
}
</style>