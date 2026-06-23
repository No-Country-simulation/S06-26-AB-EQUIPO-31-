import Image from "next/image"

export default function ShowIcon(){
    return (
        <Image src="/logo.png" alt="Logo" width={80} height={100}  style={{
    display: "block",
    margin: 0,
    padding: 0,
  }}/>
        );
}