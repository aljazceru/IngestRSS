async function fetchFeeds() {
    const res = await fetch('/api/feeds');
    const feeds = await res.json();
    const tbody = document.querySelector('#feeds-table tbody');
    tbody.innerHTML = '';
    feeds.forEach(feed => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${feed.url}</td>
            <td><button onclick="deleteFeed('${feed.url}')">Delete</button></td>`;
        tbody.appendChild(tr);
    });
}

async function addFeed() {
    const url = document.getElementById('feed-url').value;
    if (!url) return alert('Enter a URL');
    await fetch('/api/feeds', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url})
    });
    document.getElementById('feed-url').value = '';
    fetchFeeds();
}

async function deleteFeed(url) {
    await fetch('/api/feeds', {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url})
    });
    fetchFeeds();
}

window.onload = fetchFeeds;
