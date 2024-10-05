"use client"

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const links = [
    {
        name: "login",
        path: "/login",
    },
    {
        name: "about",
        path: "/about",
    }
]

const Nav = () => {
    const pathname = usePathname();
  return (
    <nav className="flex gap-8">
        {links.map((link, index) => {
            return (
                <Link 
                    href={link.path} 
                    key={index} 
                    className={`${link.path === pathname && "text-accent border-b-2 border-accent"}
                    text-2xl font-large hover:text-primary transition-all`}
                    >
                    {link.name}
                </Link>
            );
        })}
    </nav>
  )
}

export default Nav