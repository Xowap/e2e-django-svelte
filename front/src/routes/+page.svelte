<script lang="ts">
    import type { PageData } from "./$types";

    export let data: PageData;
</script>

<h1>Items!</h1>

<ul>
    {#each data.items as item}
        <li>#{item.id}: {item.name}</li>
    {/each}
</ul>
