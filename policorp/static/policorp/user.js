export async function fetchUser(username) {
  let response = await fetch(`/policorp/user/${username}/`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}
